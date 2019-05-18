import Markdown from './markdown/markdown';
import * as WebResourceInliner from 'web-resource-inliner';
import * as FileSystem from 'fs';

const mdInstantance: Markdown = new Markdown();
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


const config: WebResourceInliner.Options = {
    'fileContent': result,
    'images': true,
    'links': true,
    'scripts': true,
    'svgs': true,
    'strict': true
};
WebResourceInliner.html(config, (error: any, result: any) => {
    if (error) {
        console.error(error);
        return;
    }

    FileSystem.writeFile('output.html', result as string, err => { if (err) console.error(err) });
});
