"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Type;
(function (Type) {
    Type["BLOCK"] = "block";
    Type["INLINE"] = "inline";
})(Type = exports.Type || (exports.Type = {}));
const NAME_REGEX = /^[A-Za-z0-9_\-]+$/;
const NAME_EXTRACT_REGEX = /^\s*\{([A-Za-z0-9_\-]*)\}\s*/;
class ExtenderConfig {
    constructor() {
        this.blockExtensions = [];
        this.inlineExtensions = [];
    }
    register(extension) {
        let extensions;
        switch (extension.type) {
            case Type.BLOCK: {
                extensions = this.blockExtensions;
                break;
            }
            case Type.INLINE: {
                extensions = this.inlineExtensions;
                break;
            }
            default: {
                throw "Unrecognized type"; // should never happen
            }
        }
        if (extension.names.filter(n => n.match(NAME_REGEX)).length !== extension.names.length) {
            throw "Key must only contain " + NAME_REGEX + ": " + extension.names;
        }
        for (const name of extension.names) {
            if (extensions.filter(e => e.names.includes(name)).length !== 0) {
                throw 'Duplicate registeration of ' + extension.type + ' extension not allowed: ' + extension.names;
            }
        }
        extensions.push(extension);
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
        if (extension.names.includes(name)) {
            return extension;
        }
    }
    return undefined;
}
function findRule(markdownIt, name, rules) {
    let ret;
    for (const inlineRule of rules) {
        if (inlineRule.name === name) {
            ret = inlineRule;
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
function addRenderersToMarkdown(extensions, markdownIt, context) {
    for (const extension of extensions) {
        if (extension.render !== undefined) {
            const renderFn = extension.render;
            for (const name of extension.names) {
                markdownIt.renderer.rules[name] = function (tokens, idx) {
                    return renderFn(markdownIt, tokens, idx, context);
                };
            }
        }
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
    // Augment md's renderer to call our extension custom render functions when that extension's name is encountered
    // as a token's type.
    addRenderersToMarkdown(inlineExtensions, markdownIt, context);
    addRenderersToMarkdown(blockExtensions, markdownIt, context);
}
exports.extender = extender;
//# sourceMappingURL=extender_plugin.js.map