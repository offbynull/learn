const tocContext = {
    render: function(markdownIt, tokens, tokenIdx) {
        let ret = '';
        let inHeader = false;
        let headerLevel = 0;
        for (const token of tokens) {
            if (token.type === 'heading_open') {
                inHeader = true;
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
                continue;
            }
    
            if (inHeader === true) {
                ret += '<li>' + markdownIt.utils.escapeHtml(token.content) + '</li>\n';
            }
        }
    
        while (headerLevel > 0) {
            ret += '</ul>\n';
            headerLevel--;
        }
    
        return '<div class="toc">\n' + ret + '</div>\n';
    }
}


module.exports = function(config) {
    // why are we using an array instead of a map/object? because the exection order matters
    config.blockHandlers = config.blockHandlers || [];
    config.inlineHandlers = config.inlineHandlers || [];

    config.blockHandlers.push({
        name: 'toc',
        context: tocContext
    });
}