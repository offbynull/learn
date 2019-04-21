import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, ExtenderConfig } from "./extender_plugin";

class TocExtension implements Extension {
    readonly name: string = 'toc';

    public render(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number): string {
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


export function tocExtension(config: ExtenderConfig) {
    config.blockExtensions.push(new TocExtension());
}