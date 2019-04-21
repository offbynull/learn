import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, ExtenderConfig, Type } from './extender_plugin';

class BookmarkData {
    public readonly bookmarks: Map<string, string> = new Map<string, string>();
    public nextId: number = 0;
}

export class BookmarkReferenceIgnoreExtension implements Extension {
    public readonly name: string = 'bookmark-ref-ignore';
    public readonly type: Type = Type.INLINE;

    public process(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>): void {
        const token = tokens[tokenIdx];
        token.type = 'text_no_bookmark_reference';
        token.tag = '';
    }
}

export class BookmarkExtension implements Extension {
    public readonly name: string = 'bookmark';
    public readonly type: Type = Type.INLINE;

    public process(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>): void {
        const bookmarkData: BookmarkData = context.get('bookmark') || new BookmarkData();
        context.set('bookmark', bookmarkData);

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

        if (bookmarkData.bookmarks.has(content)) {
            throw 'Bookmark already defined: ' + content;
        }

        bookmarkData.bookmarks.set(content, 'bookmark' + bookmarkData.nextId);
        bookmarkData.nextId++;

        if (showText === true) {
            const textToken = new Token('text_no_bookmark_reference', '', 0);
            textToken.content = content;
            tokens.splice(tokenIdx + 1, 0, textToken);
        }
    }

    public postProcess(markdownIt: MarkdownIt, tokens: Token[], context: Map<string, any>): void {
        const bookmarkData: BookmarkData = context.get('bookmark') || new BookmarkData();
        context.set('bookmark', bookmarkData);

        for (let tokenIdx = 0; tokenIdx < tokens.length; tokenIdx++) {
            const token = tokens[tokenIdx];

            if (token.type === 'text_no_bookmark_reference') {
                token.type = 'text';
                continue;
            }

            if (token.type !== 'text') {
                if (token.children !== null) {
                    this.postProcess(markdownIt, token.children, context)
                }
                continue;
            }

            let newTokens: Token[] = [];
            let oldContent = token.content;
            const bookmarks = bookmarkData.bookmarks;
            for (const [bookmarkText, bookmarkId] of bookmarks) {
                let oldIdx = 0;
                while (true) {
                    let newIdx = oldContent.indexOf(bookmarkText, oldIdx);
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
    }
    
    public render(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>) {
        const bookmarkData: BookmarkData = context.get('bookmark') || new BookmarkData();
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