"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsdom_1 = require("jsdom");
const js_beautify_1 = __importDefault(require("js-beautify"));
var Type;
(function (Type) {
    Type["BLOCK"] = "block";
    Type["INLINE"] = "inline";
})(Type = exports.Type || (exports.Type = {}));
class TokenIdentifier {
    constructor(name, type) {
        this.name = name;
        this.type = type;
    }
}
exports.TokenIdentifier = TokenIdentifier;
const NAME_REGEX = /^[A-Za-z0-9_\-]+$/;
const NAME_EXTRACT_REGEX = /^\s*\{([A-Za-z0-9_\-]*)\}\s*/;
class ExtenderConfig {
    constructor() {
        this.blockExtensions = [];
        this.inlineExtensions = [];
    }
    register(extension) {
        let includeInBlock = false;
        let includeInInline = false;
        for (const tokenId of extension.tokenIds) {
            let extensions;
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
            const isDupe = extensions.filter(ext => ext.tokenIds.map(t => t.name).includes(tokenId.name)).length !== 0;
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
    viewBlockExtensions() {
        return this.blockExtensions;
    }
    viewInlineExtensions() {
        return this.inlineExtensions;
    }
}
exports.ExtenderConfig = ExtenderConfig;
function findExtension(extensions, name) {
    for (const extension of extensions) {
        if (extension.tokenIds.map(t => t.name).includes(name)) {
            return extension;
        }
    }
    return undefined;
}
function findRule(markdownIt, name, rules) {
    let ret;
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
function invokePostProcessors(extensions, markdownIt, tokens, context) {
    for (const extension of extensions) {
        if (extension.postProcess !== undefined) {
            extension.postProcess(markdownIt, tokens, context);
        }
    }
}
function invokePostHtmls(extensions, html, context) {
    for (const extension of extensions) {
        if (extension.postHtml !== undefined) {
            html = extension.postHtml(html, context);
        }
    }
    return html;
}
function addRenderersToMarkdown(inlineExtensions, blockExtensions, markdownIt, context) {
    const names = new Set();
    inlineExtensions.forEach(ext => ext.tokenIds.forEach(tId => names.add(tId.name)));
    blockExtensions.forEach(ext => ext.tokenIds.forEach(tId => names.add(tId.name)));
    for (const name of names) {
        // Calling extension.render directly in the render rule won't work because it happens in a new function...
        // the undefined guard above no longer applies. Copy the reference into a new const (we know the new ref
        // can't be undefined because of the guard) and invoke that instead
        const blockExt = blockExtensions.find(ext => ext.tokenIds.map(t => t.name).includes(name));
        const inlineExt = inlineExtensions.find(ext => ext.tokenIds.map(t => t.name).includes(name));
        markdownIt.renderer.rules[name] = function (tokens, idx) {
            const token = tokens[idx];
            if (token.block === true && blockExt !== undefined) {
                if (blockExt.render !== undefined) {
                    return blockExt.render(markdownIt, tokens, idx, context);
                }
            }
            else if (token.block === false && inlineExt !== undefined) {
                if (inlineExt.render !== undefined) {
                    return inlineExt.render(markdownIt, tokens, idx, context);
                }
            }
            throw 'Unrecognized render type'; // should never happen
        };
    }
}
function extender(markdownIt, extensionConfig) {
    const blockExtensions = extensionConfig.viewBlockExtensions();
    const inlineExtensions = extensionConfig.viewInlineExtensions();
    const context = new Map(); // simple map for sharing data between invocations
    // Augment block fence rule to call the extension processor with the matching name.
    const blockRules = markdownIt.block.ruler.getRules('');
    const oldFenceRule = findRule(markdownIt, 'fence', blockRules);
    // @ts-ignore the typedef for RuleBlock is incorrect
    const newFenceRule = function (state, startLine, endLine, silent) {
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
            }
            else if (extension !== undefined) { // if id is expected, keep it
                token.type = info;
                token.info = '';
                token.tag = '';
                if (extension.process !== undefined) { // call if handler is a function
                    extension.process(markdownIt, state.tokens, tokenIdx, context);
                }
            }
            else { // otherwise throw error
                throw 'Unidentified fence extension: ' + info;
            }
        }
        return ret;
    };
    markdownIt.block.ruler.at('fence', newFenceRule);
    // Augment inline backticks rule to call the extension processor with the matching name.
    const inlineRules = markdownIt.inline.ruler.getRules('');
    const oldBacktickRule = findRule(markdownIt, 'backtick', inlineRules);
    const newBacktickRule = function (state, silent) {
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
                }
                else if (extension !== undefined) { // if id is expected, keep it
                    token.type = info;
                    token.info = '';
                    token.tag = '';
                    token.content = token.content.slice(skipLen);
                    if (extension.process !== undefined) { // call if handler is a function
                        extension.process(markdownIt, state.tokens, tokenIdx, context);
                    }
                }
                else { // otherwise throw error
                    throw 'Unidentified fence extension: ' + info;
                }
            }
        }
        return ret;
    };
    markdownIt.inline.ruler.at('backticks', newBacktickRule);
    // Augment md's parsing to call our extension post processors after executing (to go over all tokens and
    // potentially manipulate them prior to rendering)
    const oldMdParse = markdownIt.parse;
    markdownIt.parse = function (src, env) {
        const tokens = oldMdParse.apply(markdownIt, [src, env]);
        invokePostProcessors(inlineExtensions, markdownIt, tokens, context);
        invokePostProcessors(blockExtensions, markdownIt, tokens, context);
        return tokens;
    };
    // Augment md's render output to call our extension post renderers after executing
    const oldMdRender = markdownIt.render;
    markdownIt.render = function (src, env) {
        let html = '<html><head></head><body>' + oldMdRender.apply(markdownIt, [src, env]) + '</body></html>';
        html = new jsdom_1.JSDOM(html).serialize(); // clean up
        html = invokePostHtmls(inlineExtensions, html, context);
        html = invokePostHtmls(blockExtensions, html, context);
        html = js_beautify_1.default.html_beautify(html); // format
        return html;
    };
    // Augment md's renderer to call our extension custom render functions when that extension's name is encountered
    // as a token's type.
    addRenderersToMarkdown(inlineExtensions, blockExtensions, markdownIt, context);
}
exports.extender = extender;
//# sourceMappingURL=extender_plugin.js.map