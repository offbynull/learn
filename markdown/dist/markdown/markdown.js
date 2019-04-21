"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const js_beautify_1 = __importDefault(require("js-beautify"));
const markdown_it_1 = __importDefault(require("markdown-it"));
const index_plugin_1 = require("./index_plugin");
const extender_plugin_1 = require("./extender_plugin");
const table_of_contents_extension_1 = require("./table_of_contents_extension");
const bookmark_extension_1 = require("./bookmark_extension");
class Markdown {
    constructor() {
        this.markdownIt = new markdown_it_1.default('commonmark');
        const extenderConfig = new extender_plugin_1.ExtenderConfig();
        table_of_contents_extension_1.tocExtension(extenderConfig);
        bookmark_extension_1.bookmarkExtension(extenderConfig);
        this.markdownIt.use(extender_plugin_1.extender, extenderConfig);
        this.markdownIt.use(index_plugin_1.indexer);
    }
    render(markdown) {
        let ret;
        ret = this.markdownIt.render(markdown);
        ret = '<html><head></head><body>' + ret + '</body></html>';
        ret = js_beautify_1.default.html_beautify(ret);
        return ret;
    }
}
exports.default = Markdown;
//# sourceMappingURL=markdown.js.map