import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';

export function indexer(md: MarkdownIt): void {
    const oldParse = md.parse;

    md.parse = function(src, env): Token[] {
        let ret = oldParse.apply(md, [src, env]);

        for (const token of ret) {
            switch (token.type) {
                case 'paragraph_open':
                case 'heading_open':
                case 'list_item_open':
                case 'table_open': {
                    token.attrSet('data-line', String(token.map[0])); // map[0] = startline, map[1] = endline
                    break;
                }
                default:
                    break; // do nothing
            }
        }

        return ret;
    }
}