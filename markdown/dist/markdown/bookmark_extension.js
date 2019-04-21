"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const token_1 = __importDefault(require("markdown-it/lib/token"));
class BookmarkData {
    constructor() {
        this.bookmarks = new Map();
        this.nextId = 0;
    }
}
class BookmarkReferenceIgnoreExtenderContext {
    constructor() {
        this.name = 'bookmark-ref-ignore';
    }
    process(markdownIt, tokens, tokenIdx, context) {
        const token = tokens[tokenIdx];
        token.type = 'text_no_bookmark_reference';
        token.tag = '';
    }
}
class BookmarkExtenderContext {
    constructor() {
        this.name = 'bookmark';
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
            let newTokens = [];
            let oldContent = token.content;
            const bookmarks = bookmarkData.bookmarks;
            for (const [bookmarkText, bookmarkId] of bookmarks) {
                let oldIdx = 0;
                while (true) {
                    let newIdx = oldContent.indexOf(bookmarkText, oldIdx);
                    if (newIdx === -1) {
                        const textTokens = [
                            new token_1.default('text', '', 0)
                        ];
                        textTokens[0].content = oldContent.substring(oldIdx);
                        newTokens = newTokens.concat(textTokens);
                        break;
                    }
                    // The bookmark_link types below don't have a render function because they don't need one.
                    // The tag and attr values get moved directly to HTML and apparently markdown-it recognizes
                    // the _open/_close suffix (_close will make the tag output as a closing HTML tag).
                    const bookmarkTokens = [
                        new token_1.default('text', '', 0),
                        new token_1.default('bookmark_link_open', 'a', 0),
                        new token_1.default('text', '', 0),
                        new token_1.default('bookmark_link_close', 'a', 0)
                    ];
                    bookmarkTokens[0].content = oldContent.substring(oldIdx, newIdx);
                    bookmarkTokens[1].attrSet('href', '#' + markdownIt.utils.escapeHtml(bookmarkId));
                    bookmarkTokens[2].content = bookmarkText;
                    newTokens = newTokens.concat(bookmarkTokens);
                    oldIdx = newIdx + bookmarkText.length;
                }
            }
            tokens.splice(tokenIdx, 1, ...newTokens);
            tokenIdx += newTokens.length - 1;
        }
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
function bookmarkExtension(config) {
    config.inlineExtensions.push(new BookmarkReferenceIgnoreExtenderContext());
    config.inlineExtensions.push(new BookmarkExtenderContext());
}
exports.bookmarkExtension = bookmarkExtension;
//# sourceMappingURL=bookmark_extension.js.map