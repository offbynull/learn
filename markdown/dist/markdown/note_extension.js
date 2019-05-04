"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extender_plugin_1 = require("./extender_plugin");
class NoteExtension {
    constructor() {
        this.tokenIds = [
            new extender_plugin_1.TokenIdentifier('note', extender_plugin_1.Type.BLOCK)
        ];
    }
    render(markdownIt, tokens, tokenIdx, context) {
        const token = tokens[tokenIdx];
        return '<div class="note">' + markdownIt.utils.escapeHtml(token.content) + '</div>';
    }
}
exports.NoteExtension = NoteExtension;
//# sourceMappingURL=note_extension.js.map