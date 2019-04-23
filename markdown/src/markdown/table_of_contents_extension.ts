import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, Type } from "./extender_plugin";

class TocData {
    public readonly headingAnchors: Map<Token, string> = new Map<Token, string>();
    public nextId: number = 0;
}

export class TocExtension implements Extension {
    public readonly names: ReadonlyArray<string> = [ 'toc' ];
    public readonly type: Type = Type.BLOCK;

    public postProcess(markdownIt: MarkdownIt, tokens: Token[], context: Map<string, any>): void {
        const tocData: TocData = context.get('toc') || new TocData();
        context.set('toc', tocData);

        for (let tokenIdx = 0; tokenIdx < tokens.length; tokenIdx++) {
            const token = tokens[tokenIdx];

            if (token.type === 'heading_open') {
                const linkReferenceTokens = [
                    new Token('link_open', 'a', 1),
                    new Token('link_close', 'a', -1)
                ];

                const anchorId = 'HEADREF' + tocData.nextId;
                tocData.nextId++;
                tocData.headingAnchors.set(token, anchorId);

                linkReferenceTokens[0].attrSet('name', markdownIt.utils.escapeHtml(anchorId));
                
                tokens.splice(tokenIdx, 0, ...linkReferenceTokens);
                tokenIdx += linkReferenceTokens.length;
                
                if (token.children !== null) { // typedef is wrong -- children MAY be null
                    this.postProcess(markdownIt, token.children, context); // not really required but just incase
                }
            }
        }
    }

    public render(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>): string {
        const tocData: TocData = context.get('toc') || new TocData();
        context.set('toc', tocData);

        let ret = '';
        let inHeader = false;
        let headerLevel = 0;
        let headerPath: Token[] = []; // hierarchy of heading_open nodes -- changes as traversal happens
        for (const token of tokens) {
            if (token.type === 'heading_open') {
                inHeader = true;
                headerPath.push(token);

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
                headerPath.pop();
                
                continue;
            }
    
            if (inHeader === true) {
                const headerOpenToken = headerPath[headerPath.length - 1];
                const anchorId = tocData.headingAnchors.get(headerOpenToken);
                if (anchorId === undefined) {
                    throw 'Unable to find anchor for token';
                }
                ret += '<li>'
                    + '<a href="#' + markdownIt.utils.escapeHtml(anchorId) + '">'
                    + markdownIt.utils.escapeHtml(token.content)
                    + '</a>'
                    + '</li>\n';
            }
        }
    
        while (headerLevel > 0) {
            ret += '</ul>\n';
            headerLevel--;
        }
    
        return '<div class="toc">\n' + ret + '</div>\n';
    }
}