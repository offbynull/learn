"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const token_1 = __importDefault(require("markdown-it/lib/token"));
const extender_plugin_1 = require("./extender_plugin");
class TocData {
    constructor() {
        this.headingAnchors = new Map();
        this.nextId = 0;
    }
}
class TocExtension {
    constructor() {
        this.names = ['toc'];
        this.type = extender_plugin_1.Type.BLOCK;
    }
    postProcess(markdownIt, tokens, context) {
        const tocData = context.get('toc') || new TocData();
        context.set('toc', tocData);
        for (let tokenIdx = 0; tokenIdx < tokens.length; tokenIdx++) {
            const token = tokens[tokenIdx];
            if (token.type === 'heading_open') {
                const linkReferenceTokens = [
                    new token_1.default('link_open', 'a', 1),
                    new token_1.default('link_close', 'a', -1)
                ];
                const anchorId = 'HEADREF' + tocData.nextId;
                tocData.nextId++;
                tocData.headingAnchors.set(token, anchorId);
                linkReferenceTokens[0].attrSet('name', markdownIt.utils.escapeHtml(anchorId));
                tokens.splice(tokenIdx, 0, ...linkReferenceTokens);
                tokenIdx += linkReferenceTokens.length;
                if (token.children !== null) { // typedef is wrong -- children MAY be null
                    this.postProcess(markdownIt, token.children, context); // not really required but just incase
                }
            }
        }
    }
    render(markdownIt, tokens, tokenIdx, context) {
        const tocData = context.get('toc') || new TocData();
        context.set('toc', tocData);
        let ret = '';
        let inHeader = false;
        let headerLevel = 0;
        let headerPath = []; // hierarchy of heading_open nodes -- changes as traversal happens
        for (const token of tokens) {
            if (token.type === 'heading_open') {
                inHeader = true;
                headerPath.push(token);
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
                headerPath.pop();
                continue;
            }
            if (inHeader === true) {
                const headerOpenToken = headerPath[headerPath.length - 1];
                const anchorId = tocData.headingAnchors.get(headerOpenToken);
                if (anchorId === undefined) {
                    throw 'Unable to find anchor for token';
                }
                ret += '<li>'
                    + '<a href="#' + markdownIt.utils.escapeHtml(anchorId) + '">'
                    + markdownIt.utils.escapeHtml(token.content)
                    + '</a>'
                    + '</li>\n';
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