import * as BrowserSync from 'browser-sync';

import Markdown from './markdown/markdown';
import * as WebResourceInliner from 'web-resource-inliner';
import * as FileSystem from 'fs';


//
// Start the server
//
const bs = BrowserSync.create();
bs.watch('input.md').on('change', () => {
    // Render input.md to output.html
    const input = FileSystem.readFileSync('input.md', 'utf-8').toString();
    
    const result = new Markdown().render(input);
    
    const config: WebResourceInliner.Options = {
        'fileContent': result,
        'images': true,
        'links': true,
        'scripts': true,
        'svgs': true,
        'strict': true
    };
    WebResourceInliner.html(
        config,
        (error, result) => {
            if (error) {
                console.error(error);
                return;
            }
            FileSystem.writeFileSync('output.html', result as string); // write out
            
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            BUG HERE WHERE RELOAD SHOWS BLANK PAGE, BUT BLANK PAGE HAS SOME CONTENT IN IT?;
            bs.reload('output.html');                                  // ask the browser to reload
        }
    );
});


bs.init({
    server: './',
    startPath: 'output.html',
    injectChanges: false,
    ghostMode: false,
    // reloadDelay: 1000,
    // reloadDebounce: 1000,

    // WORKAROUND FOR BUG -- https://github.com/BrowserSync/browser-sync/issues/1038
    // The embedded mathjax script has a <body> tag in it which triggers this bug. This same bug exists in competing tools (e.g.
    // live-server).
    snippetOptions: {
        rule: {
            match: /$/i,
            fn: (snippet, match) => snippet + match
        }
    }
});
