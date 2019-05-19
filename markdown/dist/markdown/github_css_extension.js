"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extender_plugin_1 = require("./extender_plugin");
class GithubCssExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('__UNUSED__githubcss', extender_plugin_1.Type.BLOCK)
        ];
    }
    postHtml(dom, context) {
        const document = dom.window.document;
        const headElement = document.getElementsByTagName('head')[0];
        const linkCssElem = document.createElement('link');
        linkCssElem.setAttribute('href', 'node_modules/github-markdown-css/github-markdown.css');
        linkCssElem.setAttribute('rel', 'stylesheet');
        headElement.appendChild(linkCssElem);
        const bodyElement = document.getElementsByTagName('body')[0];
        bodyElement.classList.add('markdown-body');
        return dom;
    }
}
exports.GithubCssExtension = GithubCssExtension;
//# sourceMappingURL=github_css_extension.js.map