"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const markdown_1 = __importDefault(require("./markdown/markdown"));
const WebResourceInliner = __importStar(require("web-resource-inliner"));
const FileSystem = __importStar(require("fs"));
const mdInstantance = new markdown_1.default();
const result = mdInstantance.render(`
# heading1
\`\`\`{toc}
\`\`\`
\`{bookmark} my message\` this is inline
## heading2
### heading3
# heading4
## heading5
<b>yo</b>
[this my link](http://github.com) jump to my message.
however, this \`{bookmark-ref-ignore} my message\` should not be highlighted
link using \`{bm} shorthand\` can be accessed using shorthand but not \`{bm-ri} shorthand\`

Here's a dot graph

\`\`\`{dot}
digraph { a -> b; }
\`\`\`

\`\`\`{note}
This is a custom note
\`\`\`

This is an inline mathjax expression: \`{mj} \\frac{a}{b}\`

This is a block mathjax expression:

\`\`\`{mj}
\\frac{c}{d}
\`\`\`

`);
const config = {
    'fileContent': result,
    'images': true,
    'links': true,
    'scripts': true,
    'svgs': true,
    'strict': true
};
WebResourceInliner.html(config, (error, result) => {
    if (error) {
        console.error(error);
        return;
    }
    FileSystem.writeFile('output.html', result, err => { if (err)
        console.error(err); });
});
//# sourceMappingURL=index.js.map