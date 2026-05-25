from __future__ import annotations

from LSP.protocol import DocumentUri
from LSP.protocol import TextEdit
from LSP.protocol import URI
from typing import Dict
from typing import List
from typing import Literal
from typing import Tuple
from typing import TypedDict


class WorkspaceConfigForDocumentRequest(TypedDict):
    uri: DocumentUri

FieldExistsInTarget = Dict[str, bool]

class WorkspaceConfigForDocumentResponse(TypedDict):
    uri: DocumentUri | None
    workspaceFile: URI | None
    workspaceFolder: URI | None
    words: FieldExistsInTarget
    ignoreWords: FieldExistsInTarget

EditTextArguments = Tuple[DocumentUri, int, List[TextEdit]]

class ConfigFileLocation(TypedDict):
    uri: DocumentUri
    name: str

AddWordsToConfigFileFromServerArguments = Tuple[List[str], DocumentUri, ConfigFileLocation]

AddWordsToVSCodeSettingsFromServerArguments = Tuple[List[str], DocumentUri, Literal['user']]
