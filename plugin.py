from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import List, Optional, Set
from lsp_utils import NpmClientHandler
import fnmatch
import os
import re
import sublime
import subprocess


def plugin_loaded():
    LspCspellPlugin.setup()


def plugin_unloaded():
    LspCspellPlugin.cleanup()


class LspCspellPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'packages/_server/dist', 'main.js')
    skip_npm_install = True

    @classmethod
    def is_allowed_to_start(
        cls,
        window: sublime.Window,
        initiating_view: Optional[sublime.View] = None,
        workspace_folders: Optional[List[WorkspaceFolder]] = None,
        configuration: Optional[ClientConfig] = None
    ) -> Optional[str]:
        if not workspace_folders:
            return "Requires a folder to start."
        # Config pattern is found here:
        # https://github.com/streetsidesoftware/vscode-spell-checker#example-cspelljson-file
        config_file_pattern = r'^(cspell|cspell\.config)\.(json|js)$'
        folder_exclude_patterns = set(
            sublime.load_settings('Preferences.sublime-settings').get("folder_exclude_patterns", [])
        )  # type: Set[str]
        folder_exclude_patterns.add('node_modules')  # definitely exclude node_modules
        config_file = find_file_in_workspace(config_file_pattern, workspace_folders[0].path, folder_exclude_patterns)
        if not config_file:
            return "No cspell configuration file present in the workspace folder."
        if not LspCspellPlugin.is_cspell_installed(config_file):
            return "'cspell' dependency is not installed in the workspace."
        return None  # return None to start the session

    @classmethod
    def is_cspell_installed(cls, file_path: str) -> bool:
        server_directory_path = cls._server_directory_path()
        resolve_module_script = os.path.join(server_directory_path, 'resolve_module.js')
        command = [cls._node_bin(), resolve_module_script, file_path, 'cspell']
        cspell_path = subprocess.check_output(command, universal_newlines=True)
        return bool(cspell_path)


def find_file_in_workspace(file_pattern: str, root_folder: str,
                           folder_exclude_patterns: Set[str] = None) -> Optional[str]:
    for path, directories, files in os.walk(root_folder):
        for folder_exclude_pattern in folder_exclude_patterns or []:
            # skip ignored folders
            directories[:] = [d for d in directories if not fnmatch.fnmatch(d, folder_exclude_pattern)]

        for file in files:
            if re.match(file_pattern, file):
                return os.path.join(path, file)
    return None
