from .types import WorkspaceConfigForDocumentRequest, WorkspaceConfigForDocumentResponse
from LSP.plugin.core.typing import Callable
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
