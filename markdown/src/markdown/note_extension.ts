import MarkdownIt from 'markdown-it';
import Token from 'markdown-it/lib/token';
import { Extension, Type } from "./extender_plugin";

export class NoteExtension implements Extension {
    public readonly names: ReadonlyArray<string> = [ 'note' ];
    public readonly type: Type = Type.BLOCK;


    public render(markdownIt: MarkdownIt, tokens: Token[], tokenIdx: number, context: Map<string, any>): string {
        const token = tokens[tokenIdx];
        return '<div class="note">' + markdownIt.utils.escapeHtml(token.content) + '</div>';
    }
}