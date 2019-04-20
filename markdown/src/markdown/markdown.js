const JsBeautify = require('js-beautify');

const MarkdownIt = require('markdown-it');
const ExtenderPlugin = require('./extender_plugin');
const TocExtension = require('./table_of_contents_extension');
const BookmarkExtension = require('./bookmark_extension');

class Markdown {
    constructor() {
        this._markdownIt = new MarkdownIt('commonmark');

        let extenderConfig = {};
        TocExtension(extenderConfig);
        BookmarkExtension(extenderConfig);
        this._markdownIt.use(ExtenderPlugin, extenderConfig);

        this._beautifyHtml = JsBeautify.html;
    }

    render(markdown) {
        let ret;
        ret = this._markdownIt.render(markdown);
        ret = '<html><head></head><body>' + ret + '</body></html>'
        ret = this._beautifyHtml(ret);
        return ret;
    }
}

module.exports = Markdown;