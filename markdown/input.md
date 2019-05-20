```{title} Test Input Page```

# heading1
```{toc}
```
`{bookmark} my message` this is inline
## heading2
### heading3
# heading4
## heading5
<b>yo</b>
[this my link](http://github.com) jump to my message.
however, this `{bookmark-ref-ignore} my message` should not be highlighted
link using `{bm} shorthand` can be accessed using shorthand but not `{bm-ri} shorthand`

Here's a dot graph

```{dot}
digraph { a -> b; }
```

```{note}
This is a custom note
```

This is an inline mathjax expression: `{mj} \frac{a}{b}`

This is a block mathjax expression:

```{mj}
\frac{c}{d}
```

testd