let Markdown = require('./markdown/markdown')
let mdInstantance = new Markdown();
result = mdInstantance.render(`
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
`);
console.log(result);