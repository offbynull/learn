import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, TokenIdentifier, Type } from "./extender_plugin";
import { JSDOM } from 'jsdom';

const MATHJAX_INSERTED = 'mathjax_inserted';

export class MathJaxExtension implements Extension {
    public readonly tokenIds: ReadonlyArray<TokenIdentifier> = [
        new TokenIdentifier('mj', Type.BLOCK),
        new TokenIdentifier('mj', Type.INLINE)
    ];

    public render(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>): string {
        const token = tokens[tokenIdx];
        let tex = token.content;

        context.set(MATHJAX_INSERTED, true);
        if (token.block === true) {
            tex = tex.replace(/\$\$/g, '\\$\\$'); // escape boundary markers that appear in text ($$ -> \$\$)
            tex = '$$' + tex + '$$'; // add boundary markers to front and end
            return '<div class="mathjax">' + markdownIt.utils.escapeHtml(tex) + '</div>';
        } else {
            tex = tex.replace(/\$/g, '\\$'); // escape boundary markers that appear in text ($ -> \$)
            tex = '$' + tex + '$'; // add boundary markers to front and end
            return '<span class="mathjax">' + markdownIt.utils.escapeHtml(tex) + '</span>';
        }
    }

    public postHtml(dom: JSDOM, context: Map<string, any>): JSDOM {
        if (!context.has(MATHJAX_INSERTED)) {
            return dom;
        }
    
        const document = dom.window.document;
    
    
        const bodyElement = document.getElementsByTagName('body')[0];
        if (!bodyElement.classList.contains('no-mathjax')) {
            bodyElement.classList.add('no-mathjax');
        }
    
    
        const headElement = document.getElementsByTagName('head')[0];
    
        const mjConfigScriptElem = document.createElement('script');
        mjConfigScriptElem.setAttribute('type', 'text/x-mathjax-config');
        mjConfigScriptElem.textContent = `
            MathJax.Hub.Config({
                // extensions: ["tex2jax.js"],
                // jax: ["input/TeX","output/HTML-CSS"],
                tex2jax: {
                    displayMath: [ ['$$','$$'] ],
                    inlineMath: [ ["$","$"] ],
                    processEscapes: true,
                    processRefs: false,
                    processEnvironments: false,
                    processClass: "mathjax",
                    ignoreClass: "no-mathjax"
                }
            });
        `;
        headElement.appendChild(mjConfigScriptElem);
 
        // This isn't using normal MathJax, but the MathJax single-file bundle provided at https://github.com/pkra/MathJax-single-file. It
        // was installed as a Node module using npm install --save pkra/MathJax-single-file#12.0.0 (npm defaults to accessing github
        // whenever this syntax is used).
        const mjScriptElem = document.createElement('script');
        mjScriptElem.setAttribute('type', 'text/javascript');
        mjScriptElem.setAttribute('src', 'node_modules/mathjax-single-file/dist/TeXSVGTeX/MathJax.js'); // using SVG because TeXCommonHTMLTeX accesses cdn for fonts (NOT embedded?)
        headElement.appendChild(mjScriptElem);


        return dom;
    }
}