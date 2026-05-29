from __future__ import annotations

from LSP.plugin import apply_text_edits
from LSP.plugin import command_handler
from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import parse_uri
from LSP.plugin import Promise
from LSP.plugin import request_handler
from lsp_utils import NodeManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing import Any
from typing import cast
from typing import final
from typing import TYPE_CHECKING
from typing_extensions import override
import sublime

if TYPE_CHECKING:
    from .types import AddWordsToConfigFileFromServerArguments
    from .types import AddWordsToVSCodeSettingsFromServerArguments
    from .types import EditTextArguments
    from .types import WorkspaceConfigForDocumentRequest
    from .types import WorkspaceConfigForDocumentResponse


def plugin_loaded():
    LspCspellPlugin.register()


def plugin_unloaded():
    LspCspellPlugin.unregister()


@final
class LspCspellPlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath('Packages', package_name, 'language-server'),
            Path('_server', 'main.cjs'),
            node_version_requirement='>16.0.0',
        )

    @request_handler('_onWorkspaceConfigForDocumentRequest')
    def on_workspace_config_for_document(
        self, params: WorkspaceConfigForDocumentRequest
    ) -> Promise[WorkspaceConfigForDocumentResponse]:
        # It looks like this method is necessary to enable code actions...
        return Promise.resolve({
            'uri': None,
            'workspaceFile': None,
            'workspaceFolder': None,
            'words': {},
            'ignoreWords': {}
        })

    @command_handler('cSpell.editText')
    def handle_edit_text_command(self, arguments: list[Any] | None) -> Promise[None]:
        if arguments and (session := self.weaksession()):
            uri, document_version, text_edits = cast('EditTextArguments', arguments)
            if session_buffer := session.get_session_buffer_for_uri_async(uri):
                view = session_buffer.get_view_in_group()
                apply_text_edits(view, text_edits, required_view_version=document_version)
        return Promise.resolve(None)

    @command_handler('cSpell.addWordsToConfigFileFromServer')
    def handle_add_words_to_config_command(self, arguments: list[Any] | None) -> Promise[None]:
        if arguments:
            new_words, _uri, config_file = cast('AddWordsToConfigFileFromServerArguments', arguments)
            _, workspace_config_path = parse_uri(config_file['uri'])
            workspace_config: dict[str, Any] = {}
            with open(workspace_config_path) as f:
                if contents := f.read():
                    workspace_config = cast('dict[str, Any]', sublime.decode_value(contents))
            with open(workspace_config_path, 'w') as f:
                workspace_config.setdefault('words', [])
                workspace_config['words'] = workspace_config['words'] + new_words
                f.write(sublime.encode_value(workspace_config, pretty=True))
        return Promise.resolve(None)

    @command_handler('cSpell.addWordsToDictionaryFileFromServer')
    def handle_add_words_to_dictionary_command(self, arguments: list[Any] | None) -> Promise[None]:
        if arguments:
            new_words, _uri, config_file = cast('AddWordsToConfigFileFromServerArguments', arguments)
            _, workspace_config_path = parse_uri(config_file['uri'])
            with open(workspace_config_path, 'a') as f:
                f.writelines("\n" + word for word in new_words)
        return Promise.resolve(None)

    @command_handler('cSpell.addWordsToVSCodeSettingsFromServer')
    def handle_add_words_to_settings_command(self, arguments: list[Any] | None) -> Promise[None]:
        if arguments:
            new_words, _, _ = cast('AddWordsToVSCodeSettingsFromServerArguments', arguments)
            settings = sublime.load_settings('LSP-cspell.sublime-settings')
            server_settings = cast('dict[str, Any]', settings.get('settings', {}))
            old_words = cast('list[str]', server_settings.get('cSpell.words', []))
            words = old_words + new_words
            server_settings['cSpell.words'] = words
            settings.set('settings', server_settings)
            sublime.save_settings('LSP-cspell.sublime-settings')
        return Promise.resolve(None)
