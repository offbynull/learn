"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const token_1 = __importDefault(require("markdown-it/lib/token"));
const extender_plugin_1 = require("./extender_plugin");
class BookmarkData {
    constructor() {
        this.bookmarks = new Map();
        this.nextId = 0;
    }
}
class BookmarkReferenceIgnoreExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('bookmark-ref-ignore', extender_plugin_1.Type.INLINE),
            new extender_plugin_1.TokenIdentifier('bm-ri', extender_plugin_1.Type.INLINE)
        ];
    }
    process(markdownIt, tokens, tokenIdx) {
        const token = tokens[tokenIdx];
        token.type = 'text_no_bookmark_reference';
        token.tag = '';
    }
}
exports.BookmarkReferenceIgnoreExtension = BookmarkReferenceIgnoreExtension;
class BookmarkExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('bookmark', extender_plugin_1.Type.INLINE),
            new extender_plugin_1.TokenIdentifier('bm', extender_plugin_1.Type.INLINE)
        ];
    }
    process(markdownIt, tokens, tokenIdx, context) {
        const bookmarkData = context.get('bookmark') || new BookmarkData();
        context.set('bookmark', bookmarkData);
        const token = tokens[tokenIdx];
        let content = token.content;
        let showText = true;
        if (content.startsWith('|no_out')) {
            content = content.substring('|no_out'.length).trim();
            showText = false;
        }
        else if (content.startsWith('|out')) {
            content = content.substring('|out'.length).trim();
            showText = true;
        }
        token.content = content;
        if (bookmarkData.bookmarks.has(content)) {
            throw 'Bookmark already defined: ' + content;
        }
        bookmarkData.bookmarks.set(content, 'bookmark' + bookmarkData.nextId);
        bookmarkData.nextId++;
        if (showText === true) {
            const textToken = new token_1.default('text_no_bookmark_reference', '', 0);
            textToken.content = content;
            tokens.splice(tokenIdx + 1, 0, textToken);
        }
    }
    postProcess(markdownIt, tokens, context) {
        const bookmarkData = context.get('bookmark') || new BookmarkData();
        context.set('bookmark', bookmarkData);
        for (let tokenIdx = 0; tokenIdx < tokens.length; tokenIdx++) {
            const token = tokens[tokenIdx];
            if (token.type === 'text_no_bookmark_reference') {
                token.type = 'text';
                continue;
            }
            if (token.type !== 'text') {
                if (token.children !== null) {
                    this.postProcess(markdownIt, token.children, context);
                }
                continue;
            }
            // Sort bookmarks by bookmark text size. We want the bookmarks with the longest texts first to avoid conflicts once
            // we start searching. For example if we had the following bookmark texts...
            //     ['This', 'This is a Train', 'Train']
            // ... and we wanted to search the following string for them ...
            //     'Hello! This is a Train!!'
            // We would always first find the substring 'This is a Train' instead of just 'This' or 'Train'.
            const bookmarks = bookmarkData.bookmarks;
            const sortedBookmarks = Array.from(bookmarks);
            sortedBookmarks.sort((a, b) => b[0].length - a[0].length);
            // Scan the token and recursively break it up based on the bookmarks identified
            const newTokens = [token];
            for (let newTokenIdx = 0; newTokenIdx < newTokens.length; newTokenIdx++) {
                const newToken = newTokens[newTokenIdx];
                // We only care about text tokens -- if it isn't text, skip it.
                if (newToken.type !== 'text') {
                    continue;
                }
                // Go through each bookmark -- if the text token contains the bookmark text then break it up such that
                // the bookmark text is a link to the bookmark id. Note that the generated tokens will contain text tokens
                // themselves, specifically a text token that contains the matched bookmark text. For example...
                //     'This is my bookmark!!!'
                // ...would get tokenized as...
                //     text: 'this is my '
                //     link_open: href=#bookmarkId
                //     text: 'bookmark'
                //     link_close:
                //     text: '!!!'
                // The problem with this is that if we're going to re-scan over these generated tokens later on (because
                // even though we've generated tokens and replaced the original token based on the matched bookmark text,
                // there still may be references to other bookmark texts in our newly generated tokens). We don't want to
                // match again on the original substring we broke out (infinite loop), so that specific token has its type
                // set to a temporary value of 'BOOKMARK_TEXT_REPLACEME'...
                //     text: 'this is my '
                //     link_open: href=#bookmarkId
                //     BOOKMARK_TEXT_REPLACEME: 'bookmark' <-- NOT SET TO text TYPE BECAUSE WE DON'T WANT ANYMORE MATCHES
                //     link_close:
                //     text: '!!!'
                // The type will be reverted back to a normal 'text' type once the entire process completes.
                let replacementTokens = [];
                for (const [bookmarkText, bookmarkId] of sortedBookmarks) {
                    replacementTokens = this.tokenizeToBookmarkLink(markdownIt, bookmarkText, bookmarkId, newToken.content, 'BOOKMARK_TEXT_REPLACEME');
                    if (replacementTokens.length !== 0) {
                        break; // bookmark was found, stop searching
                    }
                }
                if (replacementTokens.length !== 0) { // if there were replacement tokens produced, then replace the token
                    // Replace the token and then move the index back so we can re-scan the from the newly generated
                    // tokens. More bookmarks may match on the the same text.
                    newTokens.splice(newTokenIdx, 1, ...replacementTokens);
                    newTokenIdx--;
                }
            }
            // Now that the scan's complete, we can correct the types (there is no chance of an infinite loop at this point)
            for (const newToken of newTokens) {
                if (newToken.type === 'BOOKMARK_TEXT_REPLACEME') {
                    newToken.type = 'text';
                }
            }
            // Replace in full tokens
            tokens.splice(tokenIdx, 1, ...newTokens); // Replace old token with new tokens 
            tokenIdx += newTokens.length - 1; // Adjust the index to account for the change
        }
    }
    tokenizeToBookmarkLink(markdownIt, bookmarkText, bookmarkId, content, tempType) {
        let oldIdx = 0;
        let nextIdx = content.indexOf(bookmarkText, oldIdx);
        if (nextIdx === -1) {
            return [];
        }
        let replacementTokens = [];
        do {
            // The bookmark_link types below don't have a render function because they don't need one.
            // The tag and attr values get moved directly to HTML and apparently markdown-it recognizes
            // the _open/_close suffix (_close will make the tag output as a closing HTML tag).
            //
            // Notice the token type for the broken out text is BOOKMARK_TEXT_REPLACEME. We need to
            // assign a temporary type to the broken out text because that generated token will
            // likely get re-scanned
            const bookmarkTokens = [
                new token_1.default('text', '', 0),
                new token_1.default('bookmark_link_open', 'a', 1),
                new token_1.default(tempType, '', 0),
                new token_1.default('bookmark_link_close', 'a', -1)
            ];
            bookmarkTokens[0].content = content.substring(oldIdx, nextIdx);
            bookmarkTokens[1].attrSet('href', '#' + markdownIt.utils.escapeHtml(bookmarkId));
            bookmarkTokens[2].content = bookmarkText;
            replacementTokens = replacementTokens.concat(bookmarkTokens);
            oldIdx = nextIdx + bookmarkText.length;
            nextIdx = content.indexOf(bookmarkText, oldIdx);
        } while (nextIdx !== -1);
        const remainderText = content.substring(oldIdx);
        if (remainderText.length !== 0) {
            const remainderTextToken = new token_1.default('text', '', 0);
            remainderTextToken.content = remainderText;
            replacementTokens.push(remainderTextToken);
        }
        return replacementTokens;
    }
    render(markdownIt, tokens, tokenIdx, context) {
        const bookmarkData = context.get('bookmark') || new BookmarkData();
        context.set('bookmark', bookmarkData);
        const token = tokens[tokenIdx];
        const content = token.content;
        const bookmarkId = bookmarkData.bookmarks.get(content);
        if (bookmarkId === undefined) {
            throw 'Undefined bookmark when rendering'; // this should never happen
        }
        return '<a name="' + markdownIt.utils.escapeHtml(bookmarkId) + '"></a>';
    }
}
exports.BookmarkExtension = BookmarkExtension;
//# sourceMappingURL=bookmark_extension.js.map