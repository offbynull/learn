import MarkdownIt from 'markdown-it';

import { indexer } from './index_plugin';
import { extender, ExtenderConfig } from './extender_plugin';
import { TocExtension } from './table_of_contents_extension';
import { BookmarkExtension, BookmarkReferenceIgnoreExtension } from './bookmark_extension';
import { DotExtension } from './dot_graph_extension';
import { NoteExtension } from './note_extension';
import { MathJaxExtension } from './mathjax_extension';
import { GithubCssExtension } from './github_css_extension';
import { TitleExtension } from './title_extension';

export default class Markdown {
    private readonly markdownIt: MarkdownIt;

    public constructor() {
        this.markdownIt = new MarkdownIt('commonmark');

        const extenderConfig: ExtenderConfig = new ExtenderConfig();
        extenderConfig.register(new TitleExtension());
        extenderConfig.register(new GithubCssExtension());
        extenderConfig.register(new BookmarkExtension());
        extenderConfig.register(new BookmarkReferenceIgnoreExtension());
        extenderConfig.register(new TocExtension());
        extenderConfig.register(new DotExtension());
        extenderConfig.register(new NoteExtension());
        extenderConfig.register(new MathJaxExtension());
        this.markdownIt.use(extender, extenderConfig);
        this.markdownIt.use(indexer);
    }

    public render(markdown: string): string {
        return this.markdownIt.render(markdown);
    }
}