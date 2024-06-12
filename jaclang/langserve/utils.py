"""Utility functions for the language server."""

import asyncio
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Optional,
    ParamSpec,
    TYPE_CHECKING,
    TypeVar,
)

import jaclang.compiler.absyntree as ast
from jaclang.compiler.symtable import SymbolTable

if TYPE_CHECKING:
    from jaclang.langserve.engine import JacLangServer

T = TypeVar("T", bound=Callable[..., Coroutine[Any, Any, Any]])
P = ParamSpec("P")


def debounce(wait: float) -> Callable[[T], Callable[..., Awaitable[None]]]:
    """Debounce decorator for async functions."""

    def decorator(fn: T) -> Callable[..., Awaitable[None]]:
        @wraps(fn)
        async def debounced(*args: P.args, **kwargs: P.kwargs) -> None:
            async def call_it() -> None:
                await fn(*args, **kwargs)

            if hasattr(debounced, "_task"):
                debounced._task.cancel()

            async def debounced_coro() -> None:
                try:
                    await asyncio.sleep(wait)
                    await call_it()
                except asyncio.CancelledError:
                    pass

            setattr(  # noqa: B010
                debounced, "_task", asyncio.create_task(debounced_coro())
            )

        return debounced

    return decorator


def sym_tab_list(sym_tab: SymbolTable, file_path: str) -> list[SymbolTable]:
    """Iterate through symbol table."""
    sym_tabs = (
        [sym_tab]
        if not (
            isinstance(sym_tab.owner, ast.Module)
            and sym_tab.owner.loc.mod_path != file_path
        )
        else []
    )
    for i in sym_tab.kid:
        sym_tabs += sym_tab_list(i, file_path=file_path)
    return sym_tabs


def position_within_node(node: ast.AstNode, line: int, character: int) -> bool:
    """Check if the position falls within the node's location."""
    if node.loc.first_line < line + 1 < node.loc.last_line:
        return True
    if (
        node.loc.first_line == line + 1
        and node.loc.col_start <= character
        and (
            node.loc.last_line == line + 1
            and node.loc.col_end >= character
            or node.loc.last_line > line + 1
        )
    ):
        return True
    if (
        node.loc.last_line == line + 1
        and node.loc.col_start <= character <= node.loc.col_end
    ):
        return True
    return False


def get_node_info(ls: "JacLangServer", node: ast.AstNode) -> Optional[str]:
    """Extract meaningful information from the AST node."""
    try:
        if isinstance(node, ast.Token):
            if isinstance(node, ast.AstSymbolNode):
                if isinstance(node, ast.String):
                    return None
                if node.sym_link and node.sym_link.decl:
                    decl_node = node.sym_link.decl
                    if isinstance(decl_node, ast.Architype):
                        if decl_node.doc:
                            node_info = (
                                f"(architype) {node.value} \n{decl_node.doc.lit_value}"
                            )
                        else:
                            node_info = f"(architype) {node.value}"
                    elif isinstance(decl_node, ast.Ability):
                        node_info = f"(ability) can {node.value}"
                        if decl_node.signature:
                            node_info += f" {decl_node.signature.unparse()}"
                        if decl_node.doc:
                            node_info += f"\n{decl_node.doc.lit_value}"
                    elif isinstance(decl_node, ast.Name):
                        node_info = f"{node.value}"
                    elif isinstance(decl_node, ast.HasVar):
                        if decl_node.type_tag:
                            node_info = f"(variable) {decl_node.name.value} {decl_node.type_tag.unparse()}"
                        else:
                            node_info = f"(variable) {decl_node.name.value}"
                    else:
                        ls.log_warning(f"no match found decl node is \n {decl_node}")
                else:
                    node_info = f"Name: {node.value}\n"
            else:
                return None
        else:
            # ls.log_warning(f'Something happened in function -[position_within_node] ')
            return None
    except AttributeError as e:
        ls.log_error(f"Attribute error when accessing node attributes: {e}")
    return node_info.strip()
