from LSP.plugin.core.views import parse_uri
import sublime
from .types import AddWordsToConfigFileFromServerArguments, AddWordsToVSCodeSettingsFromServerArguments, EditTextArguments, WorkspaceConfigForDocumentRequest, WorkspaceConfigForDocumentResponse
from LSP.plugin.core.typing import Any, Callable, Mapping, cast, Dict
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
    server_binary_path = os.path.join(server_directory, '_server', 'dist', 'main.js')

    @classmethod
    def required_node_version(cls) -> str:
        return ">16.0.0"

    @request_handler('onWorkspaceConfigForDocumentRequest')
    def on_workspace_config_for_document(
        self, params: WorkspaceConfigForDocumentRequest, respond: Callable[[WorkspaceConfigForDocumentResponse], None]
    ) -> None:
        # It looks like this method is necessary to enable code actions...
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

        session = self.weaksession()
        if not session:
            return command_is_unhandled()

        def handle_edit_text(arguments: EditTextArguments) -> bool:
            _uri, _document_version, text_edits = arguments
            view = sublime.active_window().active_view()
            if not view:
                return command_is_handled()
            apply_text_edits_to_view(text_edits, view)  # todo: not public API
            return command_is_handled()

        if params['command'] == 'cSpell.editText':
            return handle_edit_text(cast(EditTextArguments, params['arguments']))

        def add_words_to_config_file(arguments: AddWordsToConfigFileFromServerArguments) -> bool:
            new_words, uri, config_file = arguments
            _, workspace_config_path = parse_uri(config_file['uri'])
            workspace_config = {}
            with open(workspace_config_path) as f:
                contents = f.read()
                if contents:
                    workspace_config = sublime.decode_value(contents)
            with open(workspace_config_path, 'w') as f:
                workspace_config.setdefault('words', [])
                workspace_config['words'] = workspace_config['words'] + new_words
                f.write(sublime.encode_value(workspace_config, pretty=True))
            return command_is_handled()

        if params['command'] == 'cSpell.addWordsToConfigFileFromServer':
            return add_words_to_config_file(cast(AddWordsToConfigFileFromServerArguments, params['arguments']))

        def add_words_to_dictionary_file(arguments: AddWordsToConfigFileFromServerArguments) -> bool:
            new_words, uri, config_file = arguments
            _, workspace_config_path = parse_uri(config_file['uri'])
            with open(workspace_config_path, 'a') as f:
                for word in new_words:
                    f.write("\n" + word)
            return command_is_handled()

        if params['command'] == "cSpell.addWordsToDictionaryFileFromServer":
            return add_words_to_dictionary_file(cast(AddWordsToConfigFileFromServerArguments, params['arguments']))

        def add_words_to_user_settings(arguments: AddWordsToVSCodeSettingsFromServerArguments) -> bool:
            new_words, _, _ = arguments
            settings = sublime.load_settings('LSP-cspell.sublime-settings')
            server_settings = settings.get('settings', {})  # type: Dict[str, str]
            old_words = server_settings.get('cSpell.words') or []
            words = old_words + new_words  # type: ignore
            server_settings['cSpell.words'] = words
            settings.set('settings', server_settings)
            sublime.save_settings('LSP-cspell.sublime-settings')
            return command_is_handled()

        if params['command'] == 'cSpell.addWordsToVSCodeSettingsFromServer':
            return add_words_to_user_settings(cast(AddWordsToVSCodeSettingsFromServerArguments, params['arguments']))

        return command_is_unhandled()
