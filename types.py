from LSP.plugin.core.protocol import URI, TextEdit
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
CSpell_EditText_Arguments = Tuple[URI, DocumentVersion, List[TextEdit]]