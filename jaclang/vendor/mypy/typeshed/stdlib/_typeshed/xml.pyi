# See the README.md file in this directory for more information.

from typing import Any, Protocol

# As defined https://docs.python.org/3/library/xml.dom.html#domimplementation-objects
class DOMImplementation(Protocol):
    def hasFeature(self, __feature: str, __version: str | None) -> bool: ...
    def createDocument(
        self, __namespaceUri: str, __qualifiedName: str, __doctype: Any | None
    ) -> Any: ...
    def createDocumentType(
        self, __qualifiedName: str, __publicId: str, __systemId: str
    ) -> Any: ...
