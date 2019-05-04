import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, TokenIdentifier, Type } from "./extender_plugin";

// import Viz from 'viz.js';
import { Module, render } from 'viz.js/full.render.js';

export class DotExtension implements Extension {
    public readonly tokenIds: ReadonlyArray<TokenIdentifier> = [
        new TokenIdentifier('dot', Type.BLOCK)
    ];

    public render(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>): string {
        // The following code had to be ripped out of viz.js's internals because the only public interfaces viz.js
        // exposes are those that return Promises. Even though the promise it returns is resolved immediately (upon
        // creation), it's impossible to grab the value out of the promise -- there's no other way to get a non-async
        // interface to viz.js
        const data = tokens[tokenIdx].content;
        const instance = Module();
        const output = render(instance, data,
            {
                format: 'svg',
                engine: 'dot',
                files: [],
                images: [],
                yInvert: false,
                nop: 0
            }
        );

        return output;
    }
}