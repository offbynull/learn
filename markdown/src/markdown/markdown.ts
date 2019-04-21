import JsBeautify from 'js-beautify';
import MarkdownIt from 'markdown-it';

import { indexer } from './index_plugin';
import { extender, ExtenderConfig } from './extender_plugin';
import { tocExtension } from './table_of_contents_extension';
import { bookmarkExtension } from './bookmark_extension';

export default class Markdown {
    private readonly markdownIt: MarkdownIt;

    public constructor() {
        this.markdownIt = new MarkdownIt('commonmark');

        const extenderConfig: ExtenderConfig = new ExtenderConfig();
        tocExtension(extenderConfig);
        bookmarkExtension(extenderConfig);
        this.markdownIt.use(extender, extenderConfig);
        this.markdownIt.use(indexer);
    }

    public render(markdown: string) {
        let ret: string;
        ret = this.markdownIt.render(markdown);
        ret = '<html><head></head><body>' + ret + '</body></html>'
        ret = JsBeautify.html_beautify(ret);
        return ret;
    }
}