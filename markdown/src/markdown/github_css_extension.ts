import { Extension, TokenIdentifier, Type } from "./extender_plugin";
import { JSDOM } from 'jsdom';

export class GithubCssExtension implements Extension {
    public readonly tokenIds: ReadonlyArray<TokenIdentifier> = [
        new TokenIdentifier('__UNUSED__githubcss', Type.BLOCK)
    ];

    public postHtml(dom: JSDOM, context: Map<string, any>): JSDOM {
        const document = dom.window.document;
    
    
        const headElement = document.getElementsByTagName('head')[0];

        const linkCssElem = document.createElement('link');
        linkCssElem.setAttribute('href', 'node_modules/github-markdown-css/github-markdown.css');
        linkCssElem.setAttribute('rel', 'stylesheet');
        headElement.appendChild(linkCssElem);


        const bodyElement = document.getElementsByTagName('body')[0];
        bodyElement.classList.add('markdown-body');


        return dom;
    }
}