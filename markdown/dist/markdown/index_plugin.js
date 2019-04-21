"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function indexer(md) {
    const oldParse = md.parse;
    md.parse = function (src, env) {
        let ret = oldParse.apply(md, [src, env]);
        let idx = 0;
        for (const token of ret) {
            switch (token.type) {
                case 'paragraph_open':
                case 'heading_open':
                case 'list_item_open':
                case 'table_open': {
                    token.attrSet('data-index', String(idx));
                    idx++;
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