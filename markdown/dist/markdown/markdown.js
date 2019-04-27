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
const dot_graph_extension_1 = require("./dot_graph_extension");
const note_extension_1 = require("./note_extension");
class Markdown {
    constructor() {
        this.markdownIt = new markdown_it_1.default('commonmark');
        const extenderConfig = new extender_plugin_1.ExtenderConfig();
        extenderConfig.register(new bookmark_extension_1.BookmarkExtension());
        extenderConfig.register(new bookmark_extension_1.BookmarkReferenceIgnoreExtension());
        extenderConfig.register(new table_of_contents_extension_1.TocExtension());
        extenderConfig.register(new dot_graph_extension_1.DotExtension());
        extenderConfig.register(new note_extension_1.NoteExtension());
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