import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, Type } from "./extender_plugin";

export class TocExtension implements Extension {
    public readonly names: ReadonlyArray<string> = [ 'toc' ];
    public readonly type: Type = Type.BLOCK;

    public render(markdownIt: MarkdownIt, tokens: Token[]): string {
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
                } else if (newHeaderLevel < headerLevel) {
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