import Markdown from './markdown/markdown';
import * as WebResourceInliner from 'web-resource-inliner';
import * as FileSystem from 'fs';

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
        FileSystem.writeFileSync('output.html', result as string);
    }
);
