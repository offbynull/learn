"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extender_plugin_1 = require("./extender_plugin");
class TocExtension {
    constructor() {
        this.name = 'toc';
        this.type = extender_plugin_1.Type.BLOCK;
    }
    render(markdownIt, tokens) {
        let ret = '';
        let inHeader = false;
        let headerLevel = 0;
        for (const token of tokens) {
            if (token.type === 'heading_open') {
                inHeader = true;
                const newHeaderLevel = token.markup.length; // the number of # chars defines the header level
                if (newHeaderLevel > headerLevel) {
                    while (headerLevel < newHeaderLevel) {
                        ret += '<ul>\n';
                        headerLevel++;
                    }
                }
                else if (newHeaderLevel < headerLevel) {
                    while (headerLevel > newHeaderLevel) {
                        ret += '</ul>\n';
                        headerLevel--;
                    }
                }
                continue;
            }
            if (token.type === 'heading_close') {
                inHeader = false;
                continue;
            }
            if (inHeader === true) {
                ret += '<li>' + markdownIt.utils.escapeHtml(token.content) + '</li>\n';
            }
        }
        while (headerLevel > 0) {
            ret += '</ul>\n';
            headerLevel--;
        }
        return '<div class="toc">\n' + ret + '</div>\n';
    }
}
exports.TocExtension = TocExtension;
//# sourceMappingURL=table_of_contents_extension.js.map