import MarkdownIt, { RuleBlock, RuleInline } from 'markdown-it';
import Token from 'markdown-it/lib/token';
import StateCore = require('markdown-it/lib/rules_core/state_core');
import { JSDOM } from 'jsdom';
import JsBeautify from 'js-beautify';

export enum Type {
    BLOCK = 'block',
    INLINE = 'inline'
}

export class TokenIdentifier {
    public readonly name: string;
    public readonly type: Type;

    public constructor(name: string, type: Type) {
        this.name = name;
        this.type = type;
    }
}

export interface Extension {
    readonly tokenIds: ReadonlyArray<TokenIdentifier>;
    process?: (markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>) => void;
    postProcess?: (markdownIt: MarkdownIt, tokens: Token[], context: Map<string, any>) => void;
    render?: (markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>) => string;
    postHtml?: (html: string, context: Map<string, any>) => string;
}

const NAME_REGEX = /^[A-Za-z0-9_\-]+$/;
const NAME_EXTRACT_REGEX = /^\s*\{([A-Za-z0-9_\-]*)\}\s*/;

export class ExtenderConfig {
    private readonly blockExtensions: Extension[] = [];
    private readonly inlineExtensions: Extension[] = [];

    public register(extension: Extension): void {
        let includeInBlock = false;
        let includeInInline = false;

        for (const tokenId of extension.tokenIds) {
            let extensions: Extension[];
            switch (tokenId.type) {
                case Type.BLOCK: {
                    extensions = this.blockExtensions;
                    includeInBlock = true;
                    break;
                }
                case Type.INLINE: {
                    extensions = this.inlineExtensions;
                    includeInInline = true;
                    break;
                }
                default: {
                    throw "Unrecognized type"; // should never happen
                }
            }

            if (!tokenId.name.match(NAME_REGEX)) {
                throw "Key must only contain " + NAME_REGEX + ": " + tokenId.name;
            }

            const isDupe = extensions.filter(ext =>
                ext.tokenIds.map(t => t.name).includes(tokenId.name)
            ).length !== 0;
            if (isDupe === true) {
                throw 'Duplicate registeration of ' + tokenId.type + ' extension not allowed: ' + tokenId.name;
            }
        }

        if (includeInBlock) {
            this.blockExtensions.push(extension);
        }
        if (includeInInline) {
            this.inlineExtensions.push(extension);
        }
    }

    public viewBlockExtensions(): ReadonlyArray<Extension> {
        return this.blockExtensions;
    }

    public viewInlineExtensions(): ReadonlyArray<Extension> {
        return this.inlineExtensions;
    }
}



function findExtension(extensions: ReadonlyArray<Extension>, name: string): Extension | undefined {
    for (const extension of extensions) {
        if (extension.tokenIds.map(t => t.name).includes(name)) {
            return extension;
        }
    }
    return undefined;
}

function findRule<S extends StateCore>(markdownIt: MarkdownIt, name: string, rules: MarkdownIt.Rule<S>[]): MarkdownIt.Rule<S> {
    let ret: MarkdownIt.Rule<S> | undefined;
    for (const rule of rules) {
        if (rule.name === name) {
            ret = rule;
            break;
        }
    }
    if (ret === undefined) {
        throw name + ' rule not found';
    }
    return ret;
}

function invokePostProcessors(extensions: ReadonlyArray<Extension>, markdownIt: MarkdownIt, tokens: Token[], context: Map<string, any>): void {
    for (const extension of extensions) {
        if (extension.postProcess !== undefined) {
            extension.postProcess(markdownIt, tokens, context);
        }
    }
}

function invokePostHtmls(extensions: ReadonlyArray<Extension>, html: string, context: Map<string, any>): string {
    for (const extension of extensions) {
        if (extension.postHtml !== undefined) {
            html = extension.postHtml(html, context);
        }
    }
    return html;
}

function addRenderersToMarkdown(inlineExtensions: ReadonlyArray<Extension>, blockExtensions: ReadonlyArray<Extension>, markdownIt: MarkdownIt, context: Map<string, any>) {
    const names = new Set<string>();
    inlineExtensions.forEach(ext => ext.tokenIds.forEach(tId => names.add(tId.name)));
    blockExtensions.forEach(ext => ext.tokenIds.forEach(tId => names.add(tId.name)));

    for (const name of names) {
        // Calling extension.render directly in the render rule won't work because it happens in a new function...
        // the undefined guard above no longer applies. Copy the reference into a new const (we know the new ref
        // can't be undefined because of the guard) and invoke that instead
        const blockExt = blockExtensions.find(ext => ext.tokenIds.map(t => t.name).includes(name));
        const inlineExt = inlineExtensions.find(ext => ext.tokenIds.map(t => t.name).includes(name));
        markdownIt.renderer.rules[name] = function(tokens, idx): string {
            const token = tokens[idx];
            if (token.block === true && blockExt !== undefined) {
                if (blockExt.render !== undefined) {
                    return blockExt.render(markdownIt, tokens, idx, context);
                }
            } else if (token.block === false && inlineExt !== undefined) {
                if (inlineExt.render !== undefined) {
                    return inlineExt.render(markdownIt, tokens, idx, context);
                }
            }

            throw 'Unrecognized render type'; // should never happen
        }
    }
}

export function extender(markdownIt: MarkdownIt, extensionConfig: ExtenderConfig): void {
    const blockExtensions = extensionConfig.viewBlockExtensions();
    const inlineExtensions = extensionConfig.viewInlineExtensions();

    const context: Map<string, any> = new Map(); // simple map for sharing data between invocations


    // Augment block fence rule to call the extension processor with the matching name.
    const blockRules = markdownIt.block.ruler.getRules('');
    const oldFenceRule = findRule(markdownIt, 'fence', blockRules);
    // @ts-ignore the typedef for RuleBlock is incorrect
    const newFenceRule: RuleBlock = function(state, startLine, endLine, silent): boolean | void {
        const beforeTokenLen = state.tokens.length;
        // @ts-ignore the typedef for RuleBlock is incorrect
        let ret = oldFenceRule(state, startLine, endLine, silent);
        if (ret !== true) {
            return ret;
        }
        const afterTokenLen = state.tokens.length;
        
        if (afterTokenLen !== beforeTokenLen + 1) {
            throw 'Unexpected number of tokens';
        }

        const tokenIdx = beforeTokenLen;
        const token = state.tokens[tokenIdx];
        const infoMatch = token.info.match(NAME_EXTRACT_REGEX);
        if (infoMatch !== null && infoMatch.length === 2) { //infoMatch[0] is the whole thing, infoMatch[1] is the group
            const info = infoMatch[1];
            const extension = findExtension(blockExtensions, info);
            if (info.length === 0) { // if empty id, remove it and fallback to normal
                const skipLen = infoMatch[0].length;
                token.info = token.info.slice(skipLen);
            } else if (extension !== undefined) { // if id is expected, keep it
                token.type = info;
                token.info = '';
                token.tag = '';
                if (extension.process !== undefined) { // call if handler is a function
                    extension.process(markdownIt, state.tokens, tokenIdx, context);
                }
            } else { // otherwise throw error
                throw 'Unidentified fence extension: ' + info;
            }
        }

        return ret;
    }
    markdownIt.block.ruler.at('fence', newFenceRule);


    // Augment inline backticks rule to call the extension processor with the matching name.
    const inlineRules = markdownIt.inline.ruler.getRules('');
    const oldBacktickRule: RuleInline = findRule(markdownIt, 'backtick', inlineRules);
    const newBacktickRule: RuleInline = function(state, silent): boolean | void {
        const beforeTokenLen = state.tokens.length;
        let ret = oldBacktickRule(state, silent);
        if (ret !== true) {
            return ret;
        }
        const afterTokenLen = state.tokens.length;
        
        if (!(afterTokenLen > beforeTokenLen)) {
            throw 'No tokens generated';
        }

        for (let tokenIdx = beforeTokenLen; tokenIdx < afterTokenLen; tokenIdx++) {
            const token = state.tokens[tokenIdx];
            if (token.type !== 'code_inline') {
                continue;
            }
            
            const infoMatch = token.content.match(NAME_EXTRACT_REGEX);
            if (infoMatch !== null && infoMatch.length === 2) { //infoMatch[0] is the whole thing, infoMatch[1] is the group
                const skipLen = infoMatch[0].length;
                const info = infoMatch[1];
                const extension = findExtension(inlineExtensions, info);
                if (info.length === 0) { // if empty id, remove it and fallback to normal
                    token.content = token.content.slice(skipLen);
                } else if (extension !== undefined) { // if id is expected, keep it
                    token.type = info;
                    token.info = '';
                    token.tag = '';
                    token.content = token.content.slice(skipLen);
                    if (extension.process !== undefined) { // call if handler is a function
                        extension.process(markdownIt, state.tokens, tokenIdx, context);
                    }
                } else { // otherwise throw error
                    throw 'Unidentified fence extension: ' + info;
                }
            }
        }

        return ret;
    }
    markdownIt.inline.ruler.at('backticks', newBacktickRule);


    // Augment md's parsing to call our extension post processors after executing (to go over all tokens and
    // potentially manipulate them prior to rendering)
    const oldMdParse = markdownIt.parse;
    markdownIt.parse = function(src, env): Token[] {
        const tokens = oldMdParse.apply(markdownIt, [src, env]);
        invokePostProcessors(inlineExtensions, markdownIt, tokens, context);
        invokePostProcessors(blockExtensions, markdownIt, tokens, context);
        return tokens;
    }


    // Augment md's render output to call our extension post renderers after executing
    const oldMdRender = markdownIt.render;
    markdownIt.render = function(src, env): string {
        let html = '<html><head></head><body>' + oldMdRender.apply(markdownIt, [src, env]) + '</body></html>';
        
        html = new JSDOM(html).serialize(); // clean up

        html = invokePostHtmls(inlineExtensions, html, context);
        html = invokePostHtmls(blockExtensions, html, context);
        
        html = JsBeautify.html_beautify(html); // format

        return html;
    }


    // Augment md's renderer to call our extension custom render functions when that extension's name is encountered
    // as a token's type.
    addRenderersToMarkdown(inlineExtensions, blockExtensions, markdownIt, context);
}