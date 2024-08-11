"""Jac Registry Pass.

This pass is responsible for creating object containing the senstring, scope,
type of different important nodes in the AST as we loose access to the
semstrings after PyASTGen pass. So we create those as a pickled file for
each module
"""

import os
import pickle

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.passes import Pass
from jaclang.compiler.semtable import SemInfo, SemRegistry
from jaclang.runtimelib.utils import get_sem_scope


class RegistryPass(Pass):
    """Creates a registry for each module."""

    modules_visited: list[ast.Module] = []

    def enter_module(self, node: ast.Module) -> None:
        """Create registry for each module."""
        node.registry = SemRegistry()
        self.modules_visited.append(node)

    def exit_module(self, node: ast.Module) -> None:
        """Save registry for each module."""
        module_name = node.name
        module_dir = os.path.join(
            os.path.abspath(os.path.dirname(node.source.file_path)), Con.JAC_GEN_DIR
        )
        try:
            os.makedirs(module_dir, exist_ok=True)
            with open(
                os.path.join(module_dir, f"{module_name}.registry.pkl"), "wb"
            ) as f:
                pickle.dump(node.registry, f)
        except Exception as e:
            self.warning(f"Can't save registry for {module_name}: {e}")
        self.modules_visited.pop()

    def exit_architype(self, node: ast.Architype) -> None:
        """Save architype information."""
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node.name.value,
            node.arch_type.value,
            node.semstr.lit_value if node.semstr else "",
        )
        if (
            len(self.modules_visited)
            and self.modules_visited[-1].registry
            and scope.parent
        ):
            self.modules_visited[-1].registry.add(scope.parent, seminfo)

    def exit_enum(self, node: ast.Enum) -> None:
        """Save enum information."""
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node.name.value, "Enum", node.semstr.lit_value if node.semstr else ""
        )
        if (
            len(self.modules_visited)
            and self.modules_visited[-1].registry
            and scope.parent
        ):
            self.modules_visited[-1].registry.add(scope.parent, seminfo)

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Save variable information."""
        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node.name.value,
            extracted_type,
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_ability(self, node: ast.Ability) -> None:
        """Save ability information."""
        scope = get_sem_scope(node.owner_method)    # type: ignore[arg-type]
        seminfo = SemInfo(
            node.name_ref.sym_name,
            "Ability",
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

        if (
            isinstance(node.signature, ast.EventSignature)
            and len(self.modules_visited)
            and self.modules_visited[-1].registry
        ):
            self.modules_visited[-1].registry.add(
                get_sem_scope(node), SemInfo("No Input Params", "")
            )

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Save param information."""
        scope = get_sem_scope(node)
        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        seminfo = SemInfo(
            node.name.value,
            extracted_type,
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Save assignment information."""
        if node.aug_op:
            return

        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            (
                node.target.items[0].value
                if isinstance(node.target.items[0], ast.Name)
                else ""
            ),
            extracted_type,
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_name(self, node: ast.Name) -> None:
        """Save name information. for enum stmts."""
        if (
            node.parent
            and node.parent.parent
            and node.parent.parent.__class__.__name__ == "Enum"
        ):
            scope = get_sem_scope(node)
            seminfo = SemInfo(node.value, None, "")
            if len(self.modules_visited) and self.modules_visited[-1].registry:
                self.modules_visited[-1].registry.add(scope, seminfo)

    def extract_type(self, node: ast.AstNode) -> list[str]:
        """Collect type information in assignment using bfs."""
        extracted_type = []
        if isinstance(node, (ast.BuiltinType, ast.Token)):
            extracted_type.append(node.value)
        for child in node.kid:
            extracted_type.extend(self.extract_type(child))
        return extracted_type
