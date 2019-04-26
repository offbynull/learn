import JsBeautify from 'js-beautify';
import MarkdownIt from 'markdown-it';

import { indexer } from './index_plugin';
import { extender, ExtenderConfig } from './extender_plugin';
import { TocExtension } from './table_of_contents_extension';
import { BookmarkExtension, BookmarkReferenceIgnoreExtension } from './bookmark_extension';
import { DotExtension } from './dot_graph_extension'

export default class Markdown {
    private readonly markdownIt: MarkdownIt;

    public constructor() {
        this.markdownIt = new MarkdownIt('commonmark');

        const extenderConfig: ExtenderConfig = new ExtenderConfig();
        extenderConfig.register(new BookmarkExtension());
        extenderConfig.register(new BookmarkReferenceIgnoreExtension());
        extenderConfig.register(new TocExtension());
        extenderConfig.register(new DotExtension());
        this.markdownIt.use(extender, extenderConfig);
        this.markdownIt.use(indexer);
    }

    public render(markdown: string): string {
        let ret: string;
        ret = this.markdownIt.render(markdown);
        ret = '<html><head></head><body>' + ret + '</body></html>'
        ret = JsBeautify.html_beautify(ret);
        return ret;
    }
}