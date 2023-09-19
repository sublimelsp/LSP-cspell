from LSP.plugin.core.protocol import URI, Literal, TextEdit
from LSP.plugin.core.sessions import DocumentUri
from LSP.plugin.core.typing import Dict, List, Optional, Tuple, TypedDict

WorkspaceConfigForDocumentRequest = TypedDict('WorkspaceConfigForDocumentRequest', {
    'uri': DocumentUri
})

FieldExistsInTarget = Dict[str, bool]

WorkspaceConfigForDocumentResponse = TypedDict('WorkspaceConfigForDocumentResponse', {
    'uri': Optional[DocumentUri],
    'workspaceFile': Optional[URI],
    'workspaceFolder': Optional[URI],
    'words': FieldExistsInTarget,
    'ignoreWords': FieldExistsInTarget
})

DocumentVersion = int
EditTextArguments = Tuple[URI, DocumentVersion, List[TextEdit]]

Word = str
CurrentFileURI = URI
ConfigFileLocation = TypedDict("ConfigFileLocation", {
    'uri': URI,
    'name': str
})
AddWordsToConfigFileFromServerArguments = Tuple[List[Word], CurrentFileURI, ConfigFileLocation]

AddWordsToVSCodeSettingsFromServerArguments = Tuple[List[Word], CurrentFileURI, Literal['user']]
