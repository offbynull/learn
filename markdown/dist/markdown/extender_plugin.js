"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function findExtension(extensions, name) {
    for (const extension of extensions) {
        if (name === extension.name) {
            return extension;
        }
    }
    return undefined;
}
class ExtenderConfig {
    constructor() {
        this.blockExtensions = [];
        this.inlineExtensions = [];
    }
}
exports.ExtenderConfig = ExtenderConfig;
function extender(markdownIt, extensionConfig) {
    const blockExtensions = extensionConfig.blockExtensions;
    const inlineExtensions = extensionConfig.inlineExtensions;
    // sanity check keys
    const keyRegex = /^[A-Za-z0-9_\-]+$/;
    for (const blockExtension of blockExtensions) {
        if (!blockExtension.name.match(keyRegex)) {
            throw "Key must only contain " + keyRegex + ": " + blockExtension.name;
        }
    }
    for (const inlineExtension of inlineExtensions) {
        if (!inlineExtension.name.match(keyRegex)) {
            throw "Key must only contain " + keyRegex + ": " + inlineExtension.name;
        }
    }
    const context = new Map(); // simple map for sharing data between invocations
    // Augment block fence rule to parse our fence extensions
    let oldFenceRule;
    const blockRules = markdownIt.block.ruler.getRules('');
    for (const blockRule of blockRules) {
        if (blockRule.name === 'fence') {
            oldFenceRule = blockRule;
            break;
        }
    }
    if (oldFenceRule === undefined) {
        throw 'Fence rule not found';
    }
    const foundOldFenceRule = oldFenceRule;
    // @ts-ignore the typedef for RuleBlock is incorrect
    const newFenceRule = function (state, startLine, endLine, silent) {
        const beforeTokenLen = state.tokens.length;
        // @ts-ignore the typedef for RuleBlock is incorrect
        let ret = foundOldFenceRule(state, startLine, endLine, silent);
        if (ret === false) {
            return ret;
        }
        const afterTokenLen = state.tokens.length;
        if (afterTokenLen !== beforeTokenLen + 1) {
            throw 'Unexpected number of tokens';
        }
        const tokenIdx = beforeTokenLen;
        const token = state.tokens[tokenIdx];
        const infoMatch = token.info.match(/^\s*\{([A-Za-z0-9_\-]*)\}\s*/);
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
    // Augment inline backticks rule to parse our inline extensions
    let oldBacktickRule;
    const inlineRules = markdownIt.inline.ruler.getRules('');
    for (const inlineRule of inlineRules) {
        if (inlineRule.name === 'backtick') {
            oldBacktickRule = inlineRule;
            break;
        }
    }
    if (oldBacktickRule === undefined) {
        throw 'Backtick rule not found';
    }
    const foundOldBacktickRule = oldBacktickRule;
    const newBacktickRule = function (state, silent) {
        const beforeTokenLen = state.tokens.length;
        let ret = foundOldBacktickRule(state, silent);
        if (ret === false) {
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
            const infoMatch = token.content.match(/^\s*\{([A-Za-z0-9_\-]*)\}\s*/);
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
    // Augment md's tokenization process to call our post processing functions after tokenization
    const oldMdParse = markdownIt.parse;
    markdownIt.parse = function (src, env) {
        const tokens = oldMdParse.apply(markdownIt, [src, env]);
        for (const extension of inlineExtensions) {
            if (extension.postProcess !== undefined) {
                extension.postProcess(markdownIt, tokens, context);
            }
        }
        for (const extension of blockExtensions) {
            if (extension.postProcess !== undefined) {
                extension.postProcess(markdownIt, tokens, context);
            }
        }
        return tokens;
    };
    // Augment md's renderer to render out tokens
    for (const extension of inlineExtensions) {
        if (extension.render !== undefined) {
            const renderFn = extension.render;
            markdownIt.renderer.rules[extension.name] = function (tokens, idx, options, env, self) {
                return renderFn(markdownIt, tokens, idx, context);
            };
        }
    }
    for (const extension of blockExtensions) {
        if (extension.render !== undefined) {
            const renderFn = extension.render;
            markdownIt.renderer.rules[extension.name] = function (tokens, idx, options, env, self) {
                return renderFn(markdownIt, tokens, idx, context);
            };
        }
    }
}
exports.extender = extender;
//# sourceMappingURL=extender_plugin.js.map