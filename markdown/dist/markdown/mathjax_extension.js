"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extender_plugin_1 = require("./extender_plugin");
const jsdom_1 = require("jsdom");
class MathJaxExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('mj', extender_plugin_1.Type.BLOCK),
            new extender_plugin_1.TokenIdentifier('mj', extender_plugin_1.Type.INLINE)
        ];
    }
    render(markdownIt, tokens, tokenIdx, context) {
        const token = tokens[tokenIdx];
        let mjText = token.content;
        if (token.block === true) {
            mjText = mjText.replace(/\$/g, '\\$'); // escape boundary markers that appear in text ($ -> \$)
            mjText = '$' + mjText + '$'; // add boundary markers to front and end
            return '<span class="mathjax">' + markdownIt.utils.escapeHtml(mjText) + '</span>';
        }
        else {
            mjText = mjText.replace(/\$\$/g, '\\$\\$'); // escape boundary markers that appear in text ($$ -> \$\$)
            mjText = '$$' + mjText + '$$'; // add boundary markers to front and end
            return '<div class="mathjax">' + markdownIt.utils.escapeHtml(mjText) + '</div>';
        }
    }
    postHtml(html, context) {
        const dom = new jsdom_1.JSDOM(html);
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
                extensions: ["tex2jax.js"],
                jax: ["input/TeX","output/HTML-CSS"],
                tex2jax: {
                    displayMath: [ ['$$','$$'] ]
                    inlineMath: [ ["$","$"] ],
                    processEscapes: true,
                    processRefs: false,
                    processEnvironments: false,
                    processClass: "mathjax",
                    ignoreClass: "no-mathjax"
                },
            });
        `;
        headElement.appendChild(mjConfigScriptElem);
        const mjScriptElem = document.createElement('script');
        mjScriptElem.setAttribute('type', 'text/javascript');
        mjScriptElem.setAttribute('src', 'MathJax.js');
        headElement.appendChild(mjScriptElem);
        return dom.serialize();
    }
}
exports.MathJaxExtension = MathJaxExtension;
// Adds the ability for the exension system to transform he final HTML so that we can add a class="no-mathjax" to the body tag and add the relevant
// script tags...
//
// <!DOCTYPE html>
// <html>
// <head>
// <title>MathJax Test Page</title>
// <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
// <meta http-equiv="X-UA-Compatible" content="IE=edge" />
// <meta name="viewport" content="width=device-width, initial-scale=1">
// <script type="text/x-mathjax-config">
//   MathJax.Hub.Config({
//     extensions: ["tex2jax.js"],
//     jax: ["input/TeX","output/HTML-CSS"],
//     tex2jax: {
//         inlineMath: [["$","$"],["\\(","\\)"]],
//         processEscapes: true,
//         processRefs: false,
//         processEnvironments: false,
//         processClass: "mathjax",
//         ignoreClass: "no-mathjax"
//     },
//   });
// </script>
// <script type="text/javascript" src="MathJax.js"></script>
// </head>
// <body class="no-mathjax">
// ...
// </body>
// </html>
//# sourceMappingURL=mathjax_extension.js.map