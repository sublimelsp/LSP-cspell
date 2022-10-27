import sublime
from .types import CSpell_EditText_Arguments, WorkspaceConfigForDocumentRequest, WorkspaceConfigForDocumentResponse
from LSP.plugin.core.typing import Any, Callable, Mapping, cast
from LSP.plugin.formatting import apply_text_edits_to_view
from lsp_utils import NpmClientHandler, request_handler
import os


def plugin_loaded():
    LspCspellPlugin.setup()


def plugin_unloaded():
    LspCspellPlugin.cleanup()


class LspCspellPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, '_server/dist', 'main.js')
    skip_npm_install = True

    @request_handler('onWorkspaceConfigForDocumentRequest')
    def on_workspace_config_for_document(
        self, params: WorkspaceConfigForDocumentRequest, respond: Callable[[WorkspaceConfigForDocumentResponse], None]
    ) -> None:
        # TODO: this method is necessary to enable code actions to show spell check fixes...
        # it sill doesn't work but it is a start...
        respond({
            'uri': None,
            'workspaceFile': None,
            'workspaceFolder': None,
            'words': {},
            'ignoreWords': {}
        })

    def on_pre_server_command(self, params: Mapping[str, Any], done_callback: Callable[[], None]) -> bool:

        def command_is_handled():
            done_callback()
            return True

        def command_is_unhandled():
            return False

        if params['command'] == 'cSpell.editText':
            _uri, _document_version, text_edits = cast(CSpell_EditText_Arguments, params['arguments'])
            view = sublime.active_window().active_view()
            if not view:
                return command_is_handled()
            apply_text_edits_to_view(text_edits, view)  # todo: not public API
            return command_is_handled()
        return command_is_unhandled()
