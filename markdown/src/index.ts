import Markdown from './markdown/markdown';

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
`);
console.log(result);