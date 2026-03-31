from __future__ import annotations

from LSP.protocol import TextEdit
from LSP.protocol import URI
from typing import Dict
from typing import List
from typing import Literal
from typing import Tuple
from typing import TYPE_CHECKING
from typing import TypedDict

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
