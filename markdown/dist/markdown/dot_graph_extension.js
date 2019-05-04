"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extender_plugin_1 = require("./extender_plugin");
// import Viz from 'viz.js';
const full_render_js_1 = require("viz.js/full.render.js");
class DotExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('dot', extender_plugin_1.Type.BLOCK)
        ];
    }
    render(markdownIt, tokens, tokenIdx, context) {
        // The following code had to be ripped out of viz.js's internals because the only public interfaces viz.js
        // exposes are those that return Promises. Even though the promise it returns is resolved immediately (upon
        // creation), it's impossible to grab the value out of the promise -- there's no other way to get a non-async
        // interface to viz.js
        const data = tokens[tokenIdx].content;
        const instance = full_render_js_1.Module();
        const output = full_render_js_1.render(instance, data, {
            format: 'svg',
            engine: 'dot',
            files: [],
            images: [],
            yInvert: false,
            nop: 0
        });
        return output;
    }
}
exports.DotExtension = DotExtension;
//# sourceMappingURL=dot_graph_extension.js.map