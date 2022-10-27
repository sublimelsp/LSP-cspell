from LSP.plugin.core.protocol import URI
from LSP.plugin.core.sessions import DocumentUri
from LSP.plugin.core.typing import Dict, Optional, TypedDict

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
