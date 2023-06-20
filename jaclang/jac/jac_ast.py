"""Abstract class for IR Passes for Jac."""
import pprint
from typing import Dict, List, Optional, Type

from jaclang.core.edge import EdgeDir


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(
        self: "AstNode", parent: Optional["AstNode"], kid: list, line: int
    ) -> None:
        """Initialize ast."""
        self.parent = parent
        self.kid = kid if kid else []
        self.line = line
        self.meta: Dict[str, str] = {}

    def __str__(self: "AstNode") -> str:
        """Return string representation of node."""
        return f"{str(type(self).__name__)}->[{self.line},{len(self.kid)} kids]"

    def __repr__(self: "AstNode") -> str:
        """Return string representation of node."""
        return str(self)

    def to_dict(self: "AstNode") -> dict:
        """Return dict representation of node."""
        ret = {
            "node": str(type(self).__name__),
            "kid": [x.to_dict() for x in self.kid if x],
            "line": self.line,
        }
        if type(self) == Token:
            ret["name"] = self.name
            ret["value"] = self.value
        return ret

    def is_type(self: "AstNode", typ: Type["AstNode"]) -> bool:
        """Check if node is of type."""
        return type(self) == typ

    def print(self: "AstNode", depth: Optional[int] = None) -> None:
        """Print ast."""
        pprint.PrettyPrinter(depth=depth).pprint(self.to_dict())


# Utiliiy functions
# -----------------


def replace_node(node: AstNode, new_node: Optional[AstNode]) -> AstNode | None:
    """Replace node with new_node."""
    if node.parent:
        node.parent.kid[node.parent.kid.index(node)] = new_node
    if new_node:
        new_node.parent = node.parent
    return new_node


# AST Parse Level Node Types
# --------------------------


class Token(AstNode):
    """Token node type for Jac Ast."""

    def __init__(
        self: "Token",
        name: str,
        value: str,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize token."""
        self.name = name
        self.value = value
        super().__init__(parent=parent, kid=kid, line=line)


class Parse(AstNode):
    """Parse node type for Jac Ast."""

    def __init__(
        self: "Parse",
        name: str,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize parse."""
        self.name = name
        super().__init__(parent=parent, kid=kid, line=line)


# AST Mid Level Node Types
# --------------------------
class Module(AstNode):
    """Whole Program node type for Jac Ast."""

    def __init__(
        self: "Module",
        name: str,
        doc: Token,
        body: "Elements",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize whole program node."""
        self.name = name
        self.doc = doc
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class Elements(AstNode):
    """Elements node type for Jac Ast."""

    def __init__(
        self: "Elements",
        elements: List[
            "GlobalVars | Test | ModuleCode | Import | Architype | Ability | AbilitySpec"
        ],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize elements node."""
        self.elements = elements
        super().__init__(parent=parent, kid=kid, line=line)


class GlobalVars(AstNode):
    """GlobalVars node type for Jac Ast."""

    def __init__(
        self: "GlobalVars",
        doc: "DocString",
        access: Optional[Token],
        assignments: "AssignmentList",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize global var node."""
        self.doc = doc
        self.access = access
        self.assignments = assignments
        super().__init__(parent=parent, kid=kid, line=line)


class Test(AstNode):
    """Test node type for Jac Ast."""

    def __init__(
        self: "Test",
        name: Token,
        doc: "DocString",
        description: Token,
        body: "CodeBlock",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize test node."""
        self.doc = doc
        self.name = name
        self.description = description
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class ModuleCode(AstNode):
    """Free mod code for Jac Ast."""

    def __init__(
        self: "ModuleCode",
        doc: "DocString",
        body: "CodeBlock",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize test node."""
        self.doc = doc
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class DocString(AstNode):
    """DocString node type for Jac Ast."""

    def __init__(
        self: "DocString",
        value: Optional[Token],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize docstring node."""
        self.value = value
        super().__init__(parent=parent, kid=kid, line=line)


class Import(AstNode):
    """Import node type for Jac Ast."""

    def __init__(
        self: "Import",
        lang: Token,
        path: "ModulePath",
        alias: Optional[Token],
        items: Optional["ModuleItems"],
        is_absorb: bool,  # For includes
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize import node."""
        self.lang = lang
        self.path = path
        self.alias = alias
        self.items = items
        self.is_absorb = is_absorb
        super().__init__(parent=parent, kid=kid, line=line)


class ModulePath(AstNode):
    """ModulePath node type for Jac Ast."""

    def __init__(
        self: "ModulePath",
        path: List[Token],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize module path node."""
        self.path = path
        super().__init__(parent=parent, kid=kid, line=line)


class ModuleItems(AstNode):
    """ModuleItems node type for Jac Ast."""

    def __init__(
        self: "ModuleItems",
        items: List["ModuleItem"],
        parent: Optional[AstNode],
        kid: List["ModuleItem"],
        line: int,
    ) -> None:
        """Initialize module items node."""
        self.items = items
        super().__init__(parent=parent, kid=kid, line=line)


class ModuleItem(AstNode):
    """ModuleItem node type for Jac Ast."""

    def __init__(
        self: "ModuleItem",
        name: Token,
        alias: Optional[Token],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize module item node."""
        self.name = name
        self.alias = alias
        super().__init__(parent=parent, kid=kid, line=line)


class Architype(AstNode):
    """ObjectArch node type for Jac Ast."""

    def __init__(
        self: "Architype",
        name: Token,
        typ: Token,
        doc: DocString,
        access: Token,
        base_classes: "BaseClasses",
        body: "ArchBlock",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.typ = typ
        self.doc = doc
        self.access = access
        self.base_classes = base_classes
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class ArchDecl(AstNode):
    """ArchDecl node type for Jac Ast."""

    def __init__(
        self: "ArchDecl",
        doc: DocString,
        access: Token,
        typ: Token,
        name: Token,
        base_classes: "BaseClasses",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize arch decl node."""
        self.doc = doc
        self.access = access
        self.typ = typ
        self.name = name
        self.base_classes = base_classes
        self.def_link: Optional["ArchDef"] = None
        super().__init__(parent=parent, kid=kid, line=line)


class ArchDef(AstNode):
    """ArchDef node type for Jac Ast."""

    def __init__(
        self: "ArchDef",
        doc: DocString,
        mod: Optional[Token],
        arch: "ObjectRef | NodeRef | EdgeRef | WalkerRef",
        body: "ArchBlock",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize arch def node."""
        self.doc = doc
        self.mod = mod
        self.arch = arch
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class BaseClasses(AstNode):
    """BaseArch node type for Jac Ast."""

    def __init__(
        self: "BaseClasses",
        base_classes: List[Token],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize base classes node."""
        self.base_classes = base_classes
        super().__init__(parent=parent, kid=kid, line=line)


class Ability(AstNode):
    """Ability node type for Jac Ast."""

    def __init__(
        self: "Ability",
        name: Token,
        is_func: bool,
        doc: DocString,
        access: Token,
        signature: "FuncSignature | TypeSpec",
        body: "CodeBlock",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize func arch node."""
        self.name = name
        self.is_func = is_func
        self.doc = doc
        self.access = access
        self.signature = signature
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class AbilityDecl(AstNode):
    """AbilityDecl node type for Jac Ast."""

    def __init__(
        self: "AbilityDecl",
        doc: DocString,
        access: Token,
        name: Token,
        signature: "FuncSignature | TypeSpec",
        is_func: bool,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize ability decl node."""
        self.doc = doc
        self.access = access
        self.name = name
        self.signature = signature
        self.is_func = is_func
        super().__init__(parent=parent, kid=kid, line=line)


class AbilityDef(AstNode):
    """AbilityDef node type for Jac Ast."""

    def __init__(
        self: "AbilityDef",
        doc: DocString,
        mod: Optional[Token],
        ability: "AbilityRef",
        body: "CodeBlock",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize ability def node."""
        self.doc = doc
        self.mod = mod
        self.ability = ability
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class AbilitySpec(AstNode):
    """AbilitySpec node type for Jac Ast."""

    def __init__(
        self: "AbilitySpec",
        doc: DocString,
        name: Token,
        arch: "ObjectRef | NodeRef | EdgeRef | WalkerRef",
        mod: Optional[Token],
        signature: Optional["FuncSignature"],
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize arch block node."""
        self.doc = doc
        self.name = name
        self.arch = arch
        self.mod = mod
        self.signature = signature
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class ArchBlock(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self: "ArchBlock",
        members: List["ArchHas | ArchCan | ArchCanDecl "],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize arch block node."""
        self.members = members
        super().__init__(parent=parent, kid=kid, line=line)


class ArchHas(AstNode):
    """HasStmt node type for Jac Ast."""

    def __init__(
        self: "ArchHas",
        doc: DocString,
        access: Token,
        vars: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize has statement node."""
        self.doc = doc
        self.access = access
        self.vars = vars
        super().__init__(parent=parent, kid=kid, line=line)


class HasVarList(AstNode):
    """HasVarList node type for Jac Ast."""

    def __init__(
        self: "HasVarList",
        vars: List["HasVar"],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize has var list node."""
        self.vars = vars
        super().__init__(parent=parent, kid=kid, line=line)


class HasVar(AstNode):
    """HasVar node type for Jac Ast."""

    def __init__(
        self: "HasVar",
        name: Token,
        type_tag: AstNode,
        value: Optional[AstNode],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize has var node."""
        self.name = name
        self.type_tag = type_tag
        self.value = value
        super().__init__(parent=parent, kid=kid, line=line)


class TypeSpec(AstNode):
    """TypeSpec node type for Jac Ast."""

    def __init__(
        self: "TypeSpec",
        typ: AstNode,
        nested1: AstNode,  # needed for lists
        nested2: AstNode,  # needed for dicts
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize type spec node."""
        self.typ = typ
        self.nested1 = nested1
        self.nested2 = nested2
        super().__init__(parent=parent, kid=kid, line=line)


class ArchCan(AstNode):
    """CanDS node type for Jac Ast."""

    def __init__(
        self: "ArchCan",
        name: Token,
        doc: DocString,
        access: Token,
        signature: AstNode,
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize can statement node."""
        self.name = name
        self.doc = doc
        self.access = access
        self.signature = signature
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class ArchCanDecl(AstNode):
    """CanDS node type for Jac Ast."""

    def __init__(
        self: "ArchCanDecl",
        name: Token,
        doc: DocString,
        access: Token,
        signature: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize can statement node."""
        self.name = name
        self.doc = doc
        self.access = access
        self.signature = signature
        super().__init__(parent=parent, kid=kid, line=line)


class EventSignature(AstNode):
    """EventSignature node type for Jac Ast."""

    def __init__(
        self: "EventSignature",
        event: AstNode,
        arch_tag_info: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize event signature node."""
        self.event = event
        self.arch_tag_info = arch_tag_info
        super().__init__(parent=parent, kid=kid, line=line)


class NameList(AstNode):
    """NameList node type for Jac Ast."""

    def __init__(
        self: "NameList",
        names: list,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize name list node."""
        self.names = names
        super().__init__(parent=parent, kid=kid, line=line)


class FuncSignature(AstNode):
    """FuncSignature node type for Jac Ast."""

    def __init__(
        self: "FuncSignature",
        params: AstNode,
        return_type: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize method signature node."""
        self.params = params
        self.return_type = return_type
        super().__init__(parent=parent, kid=kid, line=line)


class FuncParams(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self: "FuncParams",
        params: list,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize method params node."""
        self.params = params
        super().__init__(parent=parent, kid=kid, line=line)


class ParamVar(HasVar):
    """ParamVar node type for Jac Ast."""


class CodeBlock(AstNode):
    """CodeBlock node type for Jac Ast."""

    def __init__(
        self: "CodeBlock",
        stmts: list,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize code block node."""
        self.stmts = stmts
        super().__init__(parent=parent, kid=kid, line=line)


class IfStmt(AstNode):
    """IfStmt node type for Jac Ast."""

    def __init__(
        self: "IfStmt",
        condition: AstNode,
        body: AstNode,
        elseifs: AstNode,
        else_body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize if statement node."""
        self.condition = condition
        self.body = body
        self.elseifs = elseifs
        self.else_body = else_body
        super().__init__(parent=parent, kid=kid, line=line)


class ElseIfs(AstNode):
    """ElseIfs node type for Jac Ast."""

    def __init__(
        self: "ElseIfs",
        elseifs: List["IfStmt"],
        parent: Optional[AstNode],
        kid: List["IfStmt"],
        line: int,
    ) -> None:
        """Initialize elseifs node."""
        self.elseifs = elseifs
        super().__init__(parent=parent, kid=kid, line=line)


class ElseStmt(AstNode):
    """Else node type for Jac Ast."""

    def __init__(
        self: "ElseStmt",
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize else node."""
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class TryStmt(AstNode):
    """TryStmt node type for Jac Ast."""

    def __init__(
        self: "TryStmt",
        body: AstNode,
        excepts: AstNode,
        finally_body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize try statement node."""
        self.body = body
        self.excepts = excepts
        self.finally_body = finally_body
        super().__init__(parent=parent, kid=kid, line=line)


class ExceptList(AstNode):
    """ExceptList node type for Jac Ast."""

    def __init__(
        self: "ExceptList",
        excepts: list,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize excepts node."""
        self.excepts = excepts
        super().__init__(parent=parent, kid=kid, line=line)


class Except(AstNode):
    """Except node type for Jac Ast."""

    def __init__(
        self: "Except",
        typ: AstNode,
        name: Token,
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize except node."""
        self.typ = typ
        self.name = name
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class FinallyStmt(AstNode):
    """FinallyStmt node type for Jac Ast."""

    def __init__(
        self: "FinallyStmt",
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize finally statement node."""
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class IterForStmt(AstNode):
    """IterFor node type for Jac Ast."""

    def __init__(
        self: "IterForStmt",
        iter: AstNode,
        condition: AstNode,
        count_by: AstNode,
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize iter for node."""
        self.iter = iter
        self.condition = condition
        self.count_by = count_by
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class InForStmt(AstNode):
    """InFor node type for Jac Ast."""

    def __init__(
        self: "InForStmt",
        name: Token,
        collection: AstNode,
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize in for node."""
        self.name = name
        self.collection = collection
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class DictForStmt(AstNode):
    """DictForStmt node type for Jac Ast."""

    def __init__(
        self: "DictForStmt",
        k_name: Token,
        v_name: Token,
        collection: AstNode,
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize dict for node."""
        self.k_name = k_name
        self.v_name = v_name
        self.collection = collection
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class WhileStmt(AstNode):
    """WhileStmt node type for Jac Ast."""

    def __init__(
        self: "WhileStmt",
        condition: AstNode,
        body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize while statement node."""
        self.condition = condition
        self.body = body
        super().__init__(parent=parent, kid=kid, line=line)


class RaiseStmt(AstNode):
    """RaiseStmt node type for Jac Ast."""

    def __init__(
        self: "RaiseStmt",
        cause: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize raise statement node."""
        self.cause = cause
        super().__init__(parent=parent, kid=kid, line=line)


class AssertStmt(AstNode):
    """AssertStmt node type for Jac Ast."""

    def __init__(
        self: "AssertStmt",
        condition: AstNode,
        error_msg: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize assert statement node."""
        self.condition = condition
        self.error_msg = error_msg
        super().__init__(parent=parent, kid=kid, line=line)


class CtrlStmt(AstNode):
    """CtrlStmt node type for Jac Ast."""

    def __init__(
        self: "CtrlStmt",
        stmt: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize control statement node."""
        self.stmt = stmt
        super().__init__(parent=parent, kid=kid, line=line)


class DeleteStmt(AstNode):
    """DeleteStmt node type for Jac Ast."""

    def __init__(
        self: "DeleteStmt",
        target: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize delete statement node."""
        self.target = target
        super().__init__(parent=parent, kid=kid, line=line)


class ReportStmt(AstNode):
    """ReportStmt node type for Jac Ast."""

    def __init__(
        self: "ReportStmt",
        expr: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize report statement node."""
        self.expr = expr
        super().__init__(parent=parent, kid=kid, line=line)


class ReturnStmt(AstNode):
    """ReturnStmt node type for Jac Ast."""

    def __init__(
        self: "ReturnStmt",
        expr: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize return statement node."""
        self.expr = expr
        super().__init__(parent=parent, kid=kid, line=line)


class IgnoreStmt(AstNode):
    """IgnoreStmt node type for Jac Ast."""

    def __init__(
        self: "IgnoreStmt",
        target: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize ignore statement node."""
        self.target = target
        super().__init__(parent=parent, kid=kid, line=line)


class VisitStmt(AstNode):
    """VisitStmt node type for Jac Ast."""

    def __init__(
        self: "VisitStmt",
        typ: AstNode,
        target: AstNode,
        else_body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize visit statement node."""
        self.typ = typ
        self.target = target
        self.else_body = else_body
        super().__init__(parent=parent, kid=kid, line=line)


class RevisitStmt(AstNode):
    """ReVisitStmt node type for Jac Ast."""

    def __init__(
        self: "RevisitStmt",
        hops: AstNode,
        else_body: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize revisit statement node."""
        self.hops = hops
        self.else_body = else_body
        super().__init__(parent=parent, kid=kid, line=line)


class DisengageStmt(AstNode):
    """DisengageStmt node type for Jac Ast."""

    def __init__(
        self: "DisengageStmt",
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize disengage statement node."""
        super().__init__(parent=parent, kid=kid, line=line)


class YieldStmt(AstNode):
    """YieldStmt node type for Jac Ast."""

    def __init__(
        self: "YieldStmt",
        expr: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize yeild statement node."""
        self.expr = expr
        super().__init__(parent=parent, kid=kid, line=line)


class SyncStmt(AstNode):
    """SyncStmt node type for Jac Ast."""

    def __init__(
        self: "SyncStmt",
        target: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize sync statement node."""
        self.target = target
        super().__init__(parent=parent, kid=kid, line=line)


class Assignment(AstNode):
    """Assignment node type for Jac Ast."""

    def __init__(
        self: "Assignment",
        is_static: bool,
        target: AstNode,
        value: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize assignment node."""
        self.is_static = is_static
        self.target = target
        self.value = value
        super().__init__(parent=parent, kid=kid, line=line)


class BinaryExpr(AstNode):
    """ExprBinary node type for Jac Ast."""

    def __init__(
        self: "BinaryExpr",
        left: AstNode,
        right: AstNode,
        op: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize binary expression node."""
        self.left = left
        self.right = right
        self.op = op
        super().__init__(parent=parent, kid=kid, line=line)


class IfElseExpr(AstNode):
    """ExprIfElse node type for Jac Ast."""

    def __init__(
        self: "IfElseExpr",
        condition: "BinaryExpr | IfElseExpr",
        value: AstNode,
        else_value: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize if else expression node."""
        self.condition = condition
        self.value = value
        self.else_value = else_value
        super().__init__(parent=parent, kid=kid, line=line)


class UnaryExpr(AstNode):
    """ExprUnary node type for Jac Ast."""

    def __init__(
        self: "UnaryExpr",
        operand: AstNode,
        op: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize unary expression node."""
        self.operand = operand
        self.op = op
        super().__init__(parent=parent, kid=kid, line=line)


class SpawnObjectExpr(AstNode):
    """ExprSpawnObject node type for Jac Ast."""

    def __init__(
        self: "SpawnObjectExpr",
        target: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize spawn object expression node."""
        self.target = target
        super().__init__(parent=parent, kid=kid, line=line)


class UnpackExpr(AstNode):
    """ExprUnpack node type for Jac Ast."""

    def __init__(
        self: "UnpackExpr",
        target: AstNode,
        is_dict: bool,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize unpack expression node."""
        self.target = target
        super().__init__(parent=parent, kid=kid, line=line)


class MultiString(AstNode):
    """ExprMultiString node type for Jac Ast."""

    def __init__(
        self: "MultiString",
        strings: list,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize multi string expression node."""
        self.strings = strings
        super().__init__(parent=parent, kid=kid, line=line)


class ListVal(AstNode):
    """ListVal node type for Jac Ast."""

    def __init__(
        self: "ListVal",
        values: List[
            UnaryExpr | BinaryExpr | IfElseExpr | UnpackExpr | SpawnObjectExpr
        ],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize list value node."""
        self.values = values
        super().__init__(parent=parent, kid=kid, line=line)


class ExprList(ListVal):
    """ExprList node type for Jac Ast."""


class DictVal(AstNode):
    """ExprDict node type for Jac Ast."""

    def __init__(
        self: "DictVal",
        kv_pairs: list,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize dict expression node."""
        self.kv_pairs = kv_pairs
        super().__init__(parent=parent, kid=kid, line=line)


class Comprehension(AstNode):
    """Comprehension node type for Jac Ast."""

    def __init__(
        self: "Comprehension",
        key_expr: AstNode,
        out_expr: AstNode,
        name: Token,
        collection: AstNode,
        conditional: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize comprehension expression node."""
        self.key_expr = key_expr
        self.out_expr = out_expr
        self.name = name
        self.collection = collection
        self.conditional = conditional
        super().__init__(parent=parent, kid=kid, line=line)


class KVPair(AstNode):
    """ExprKVPair node type for Jac Ast."""

    def __init__(
        self: "KVPair",
        key: AstNode,
        value: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize key value pair expression node."""
        self.key = key
        self.value = value
        super().__init__(parent=parent, kid=kid, line=line)


class AtomTrailer(AstNode):
    """AtomTrailer node type for Jac Ast."""

    def __init__(
        self: "AtomTrailer",
        target: AstNode,
        right: list,
        null_ok: bool,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize atom trailer expression node."""
        self.target = target
        self.right = right
        self.null_ok = null_ok
        super().__init__(parent=parent, kid=kid, line=line)


class FuncCall(AstNode):
    """FuncCall node type for Jac Ast."""

    def __init__(
        self: "FuncCall",
        target: AstNode,
        params: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize function call expression node."""
        self.target = target
        self.params = params
        super().__init__(parent=parent, kid=kid, line=line)


class ParamList(AstNode):
    """ParamList node type for Jac Ast."""

    def __init__(
        self: "ParamList",
        p_args: AstNode,
        p_kwargs: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize parameter list expression node."""
        self.p_args = p_args
        self.p_kwargs = p_kwargs
        super().__init__(parent=parent, kid=kid, line=line)


class AssignmentList(ExprList):
    """AssignmentList node type for Jac Ast."""


class IndexSlice(AstNode):
    """IndexSlice node type for Jac Ast."""

    def __init__(
        self: "IndexSlice",
        start: AstNode,
        stop: AstNode,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize index slice expression node."""
        self.start = start
        self.stop = stop
        super().__init__(parent=parent, kid=kid, line=line)


class GlobalRef(AstNode):
    """GlobalRef node type for Jac Ast."""

    def __init__(
        self: "GlobalRef",
        name: Token,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize global reference expression node."""
        self.name = name
        super().__init__(parent=parent, kid=kid, line=line)


class HereRef(GlobalRef):
    """HereRef node type for Jac Ast."""


class VisitorRef(GlobalRef):
    """VisitorRef node type for Jac Ast."""


class NodeRef(GlobalRef):
    """NodeRef node type for Jac Ast."""


class EdgeRef(GlobalRef):
    """EdgeRef node type for Jac Ast."""


class WalkerRef(GlobalRef):
    """WalkerRef node type for Jac Ast."""


class FuncRef(GlobalRef):
    """FuncRef node type for Jac Ast."""


class ObjectRef(GlobalRef):
    """ObjectRef node type for Jac Ast."""


class AbilityRef(GlobalRef):
    """AbilityRef node type for Jac Ast."""


class EdgeOpRef(AstNode):
    """EdgeOpRef node type for Jac Ast."""

    def __init__(
        self: "EdgeOpRef",
        filter_cond: AstNode,
        edge_dir: EdgeDir,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize edge op reference expression node."""
        self.filter_cond = filter_cond
        self.edge_dir = edge_dir
        super().__init__(parent=parent, kid=kid, line=line)


class DisconnectOp(EdgeOpRef):
    """DisconnectOpRef node type for Jac Ast."""


class ConnectOp(AstNode):
    """ConnectOpRef node type for Jac Ast."""

    def __init__(
        self: "ConnectOp",
        spawn: AstNode,
        edge_dir: EdgeDir,
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize connect op reference expression node."""
        self.spawn = spawn
        self.edge_dir = edge_dir
        super().__init__(parent=parent, kid=kid, line=line)


class SpawnCtx(AstNode):
    """SpawnCtx node type for Jac Ast."""

    def __init__(
        self: "SpawnCtx",
        spawns: List[Assignment],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize spawn context expression node."""
        self.spawns = spawns
        super().__init__(parent=parent, kid=kid, line=line)


class FilterCtx(AstNode):
    """FilterCtx node type for Jac Ast."""

    def __init__(
        self: "FilterCtx",
        compares: List[BinaryExpr],
        parent: Optional[AstNode],
        kid: List[AstNode],
        line: int,
    ) -> None:
        """Initialize filter_cond context expression node."""
        self.compares = compares
        super().__init__(parent=parent, kid=kid, line=line)


# Test the function
if __name__ == "__main__":
    from jaclang.jac.utils import load_ast_and_print_pass_template

    print(load_ast_and_print_pass_template())