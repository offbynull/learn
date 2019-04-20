function findExtension(extensionConfig, name) {
    for (const extension of extensionConfig) {
        if (name === extension.name) {
            return extension.context;
        }
    }
    return undefined;
}

module.exports = function(markdownIt, extensionConfig) {
    blockExtensions = extensionConfig.blockHandlers || [];
    inlineExtensions = extensionConfig.inlineHandlers || [];

    // sanity check keys
    const keyRegex = /^[A-Za-z0-9_\-]+$/;
    for (key of Object.keys(blockExtensions)) {
        if (!key.match(keyRegex)) {
            throw "Key must only contain " + keyRegex + ": " + key;
        }
    }
    for (key of Object.keys(inlineExtensions)) {
        if (!key.match(keyRegex)) {
            throw "Key must only contain " + keyRegex + ": " + key;
        }
    }

    context = {}; // simple map for sharing data between invocations


    // Augment block fence rule to parse our fence extensions
    let oldFenceRule;
    const blockRules = markdownIt.block.ruler.getRules('');
    for (const blockRule of blockRules) {
        if (blockRule.name === 'fence') {
            oldFenceRule = blockRule;
            break;
        }
    }
    if (typeof oldFenceRule === 'undefined') {
        throw 'Fence rule not found';
    }
    const newFenceRule = function(state, startLine, endLine, silent) {
        const beforeTokenLen = state.tokens.length;
        let ret = oldFenceRule(state, startLine, endLine, silent);
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
            } else if (typeof extension !== 'undefined') { // if id is expected, keep it
                token.type = info;
                token.info = '';
                token.tag = '';
                if (typeof extension.process === 'function') { // call if handler is a function
                    extension.process(markdownIt, state.tokens, tokenIdx, context);
                }
            } else { // otherwise throw error
                throw 'Unidentified fence extension: ' + info;
            }
        }

        return ret;
    }
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
    if (typeof oldBacktickRule === 'undefined') {
        throw 'Backtick rule not found';
    }
    const newBacktickRule = function(state, silent) {
        const beforeTokenLen = state.tokens.length;
        let ret = oldBacktickRule(state, silent);
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
                } else if (typeof extension !== 'undefined') { // if id is expected, keep it
                    token.type = info;
                    token.info = '';
                    token.tag = '';
                    token.content = token.content.slice(skipLen);
                    if (typeof extension.process === 'function') { // call if handler is a function
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


    // Augment md's tokenization process to call our post processing functions after tokenization
    const oldMdParse = markdownIt.parse;
    markdownIt.parse = function(src, env) {
        const tokens = oldMdParse.apply(markdownIt, [src, env]);
        
        for (const extension of inlineExtensions) {
            if (typeof extension.context.postProcess === 'function') {
                extension.context.postProcess(markdownIt, tokens, context);
            }
        }

        for (const extension of blockExtensions) {
            if (typeof extension.context.postProcess === 'function') {
                extension.context.postProcess(markdownIt, tokens, context);
            }
        }

        return tokens;
    }


    // Augment md's renderer to render out tokens
    for (const extension of inlineExtensions) {
        markdownIt.renderer.rules[extension.name] = function(tokens, idx, options, env, self) {
            return extension.context.render(markdownIt, tokens, idx, context);
        }
    }

    for (const extension of blockExtensions) {
        markdownIt.renderer.rules[extension.name] = function(tokens, idx, options, env, self) {
            return extension.context.render(markdownIt, tokens, idx, context);
        }
    }
}