"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extender_plugin_1 = require("./extender_plugin");
const jsdom_1 = require("jsdom");
class GithubCssExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('__UNUSED__githubcss', extender_plugin_1.Type.BLOCK)
        ];
    }
    postHtml(html, context) {
        const dom = new jsdom_1.JSDOM(html);
        const document = dom.window.document;
        const headElement = document.getElementsByTagName('head')[0];
        const linkCssElem = document.createElement('link');
        linkCssElem.setAttribute('href', 'node_modules/github-markdown-css/github-markdown.css');
        linkCssElem.setAttribute('rel', 'stylesheet');
        headElement.appendChild(linkCssElem);
        return dom.serialize();
    }
}
exports.GithubCssExtension = GithubCssExtension;
//# sourceMappingURL=css_extension.js.map