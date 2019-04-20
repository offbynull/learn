const Token = require('markdown-it/lib/token');

const bookmarkReferenceIgnoreContext = {
    process: function(markdownIt, tokens, tokenIdx, context) {
        const token = tokens[tokenIdx];
        token.type = 'text_no_bookmark_reference';
        token.tag = '';
    }
}

const bookmarkContext = {
    process: function(markdownIt, tokens, tokenIdx, context) {
        context.bookmark = context.bookmark || {}
        const bookmarkContext = context.bookmark;

        const token = tokens[tokenIdx];
        let content = token.content;
        let showText = true;
        if (content.startsWith('|no_out')) {
            content = content.substring('|no_out'.length).trim();
            showText = false;
        } else if (content.startsWith('|out')) {
            content = content.substring('|out'.length).trim();
            showText = true;
        }
        token.content = content;

        bookmarkContext.bookmarks = bookmarkContext.bookmarks || {};
        bookmarkContext.nextId = bookmarkContext.nextId || 0;

        if (typeof bookmarkContext.bookmarks[content] !== 'undefined') {
            throw 'Bookmark already defined: ' + content;
        }

        bookmarkContext.bookmarks[content] = 'bookmark' + bookmarkContext.nextId;
        bookmarkContext.nextId++;

        if (showText === true) {
            const textToken = new Token('text_no_bookmark_reference', '', 0);
            textToken.content = content;
            tokens.splice(tokenIdx + 1, 0, textToken);
        }
    },
    postProcess: function f(markdownIt, tokens, context) {
        context.bookmark = context.bookmark || {}
        const bookmarkContext = context.bookmark;

        for (let tokenIdx = 0; tokenIdx < tokens.length; tokenIdx++) {
            const token = tokens[tokenIdx];

            if (token.type === 'text_no_bookmark_reference') {
                token.type = 'text';
                continue;
            }

            if (token.type !== 'text') {
                if (token.children !== null) {
                    f(markdownIt, token.children, context)
                }
                continue;
            }

            let newTokens = [];
            let oldContent = token.content;
            const bookmarks = bookmarkContext.bookmarks || {};
            for (const [bookmarkText, bookmarkId] of Object.entries(bookmarks)) {
                let oldIdx = 0;
                while (true) {
                    newIdx = oldContent.indexOf(bookmarkText, oldIdx);
                    if (newIdx === -1) {
                        const textTokens = [
                            new Token('text', '', 0)
                        ];
                        textTokens[0].content = oldContent.substring(oldIdx);
                        newTokens = newTokens.concat(textTokens);
                        break;
                    }
                    // The bookmark_link types below don't have a render function because they don't need one.
                    // The tag and attr values get moved directly to HTML and apparently markdown-it recognizes
                    // the _open/_close suffix (_close will make the tag output as a closing HTML tag).
                    const bookmarkTokens = [
                        new Token('text', '', 0), // pre text
                        new Token('bookmark_link_open', 'a', 0),
                        new Token('text', '', 0), // link text
                        new Token('bookmark_link_close', 'a', 0)
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
    },
    render: function(markdownIt, tokens, tokenIdx, context) {
        context.bookmark = context.bookmark || {}
        const bookmarkContext = context.bookmark;

        const token = tokens[tokenIdx];
        const content = token.content;
        
        const bookmarkId = bookmarkContext.bookmarks[content];
        return '<a name="' + markdownIt.utils.escapeHtml(bookmarkId) + '"></a>';
    }
}

module.exports = function(config) {
    // why are we using an array instead of a map/object? because the exection order matters
    config.blockHandlers = config.blockHandlers || [];
    config.inlineHandlers = config.inlineHandlers || [];

    config.inlineHandlers.push({
        name: 'bookmark-ref-ignore',
        context: bookmarkReferenceIgnoreContext
    });
    config.inlineHandlers.push({
        name: 'bookmark',
        context: bookmarkContext
    });
}