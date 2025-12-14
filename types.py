from __future__ import annotations
from LSP.plugin.core.protocol import URI, TextEdit
from typing import Dict, List, Optional, Tuple, TypedDict, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from LSP.protocol import DocumentUri


class WorkspaceConfigForDocumentRequest(TypedDict):
    uri: DocumentUri

FieldExistsInTarget = Dict[str, bool]

class WorkspaceConfigForDocumentResponse(TypedDict):
    uri: DocumentUri | None
    workspaceFile: URI | None
    workspaceFolder: URI | None
    words: FieldExistsInTarget
    ignoreWords: FieldExistsInTarget

DocumentVersion = int
EditTextArguments = Tuple[URI, DocumentVersion, List[TextEdit]]
Word = str
CurrentFileURI = URI

class ConfigFileLocation(TypedDict):
    uri: URI
    name: str

AddWordsToConfigFileFromServerArguments = Tuple[List[Word], CurrentFileURI, ConfigFileLocation]

AddWordsToVSCodeSettingsFromServerArguments = Tuple[List[Word], CurrentFileURI, Literal['user']]
