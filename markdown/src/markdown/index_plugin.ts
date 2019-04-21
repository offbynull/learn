import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';

export function indexer(md: MarkdownIt): void {
    const oldParse = md.parse;

    md.parse = function(src, env): Token[] {
        let ret = oldParse.apply(md, [src, env]);

        let idx = 0;
        for (const token of ret) {
            switch (token.type) {
                case 'paragraph_open':
                case 'heading_open':
                case 'list_item_open':
                case 'table_open': {
                    token.attrSet('data-index', String(idx))
                    idx++;
                    break;
                }
                default:
                    break; // do nothing
            }
        }

        return ret;
    }
}