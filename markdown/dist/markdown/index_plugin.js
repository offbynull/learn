"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function indexer(md) {
    const oldParse = md.parse;
    md.parse = function (src, env) {
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
    };
}
exports.indexer = indexer;
//# sourceMappingURL=index_plugin.js.map