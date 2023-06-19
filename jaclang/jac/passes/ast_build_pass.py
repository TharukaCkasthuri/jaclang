"""Pass that builds well formed AST from parse tree AST."""
from copy import copy


import jaclang.jac.ast as ast
from jaclang.jac.ast import convert_kind, make_blank, replace_node, update_kind
from jaclang.jac.passes.ir_pass import Pass


class AstBuildPass(Pass):
    """Ast build pass."""

    def __init__(
        self: "AstBuildPass", mod_name: str = None, *args: list, **kwargs: dict
    ) -> None:
        """Initialize pass."""
        self.mod_name = mod_name
        super().__init__(*args, **kwargs)

    def exit_start(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build WHOLE_BUILD Ast node."""
        self.ir = ast.Module(
            name=self.mod_name,
            doc=node.kid[0] if len(node.kid) == 2 else ast.Blank(),
            body=node.kid[1] if len(node.kid) == 2 else node.kid[0],
            parent=None,
            kid=node.kid,
            line=node.line,
        )

    def exit_doc_tag(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build DOC_TAG Ast node."""
        if node.kid[0].is_type(ast.Token):
            node.kid = [node.kid[0]]
        update_kind(node, ast.DocString, value=node.kid[0])

    def exit_element_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        update_kind(node, ast.Elements, elements=node.kid)

    def exit_element(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Replace element with its kid."""
        node = replace_node(node, node.kid[0])

    def exit_global_var(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build GLOBAL_VAR Ast node."""
        node.kid = [node.kid[0], node.kid[2], node.kid[3]]
        update_kind(
            node,
            ast.GlobalVars,
            doc=node.kid[0],
            access=node.kid[1],
            assignments=node.kid[2],
        )

    def exit_access(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build  Ast node."""
        replace_node(node, node.kid[0])

    def exit_access_tag(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build  Ast node."""
        replace_node(node, node.kid[-1])

    def exit_test(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build TEST Ast node."""
        del node.kid[1]
        update_kind(
            node,
            ast.Test,
            doc=node.kid[0],
            name=node.kid[1],
            description=node.kid[2],
            body=node.kid[3],
        )

    def exit_mod_code(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build TEST Ast node."""
        node.kid = [node.kid[0], node.kid[-1]]
        update_kind(node, ast.ModuleCode, doc=node.kid[0], body=node.kid[1])

    def exit_import_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build IMPORT Ast node."""
        kid = node.kid
        meta = {
            "lang": kid[1],
            "path": kid[2],
            "alias": ast.Blank(),
            "items": ast.Blank(),
            "is_absorb": False,
        }
        if len(node.kid) == 7:
            meta["path"] = kid[3]
            meta["items"] = kid[5]
            node.kid = [kid[1], kid[3], kid[5]]
        elif len(node.kid) == 6:
            meta["alias"] = kid[4]
            node.kid = [kid[1], kid[2], kid[4]]
        else:
            node.kid = [kid[1], kid[2]]
        update_kind(node, ast.Import, **meta)
        print("".join([i.value for i in meta["path"].kid]))

    def exit_include_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Include Ast node."""
        kid = node.kid
        meta = {
            "lang": kid[1],
            "path": kid[2],
            "alias": ast.Blank(),
            "items": ast.Blank(),
            "is_absorb": True,
        }
        node.kid = [kid[1], kid[2]]
        update_kind(node, ast.Import, **meta)

    def exit_import_path(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build MOD_PATH Ast node."""
        if len(node.kid) == 1:
            node.kid = node.kid[0].kid
        else:
            node.kid = node.kid[0].kid + node.kid[1].kid
        update_kind(node, ast.ModulePath, path=node.kid)

    def exit_import_path_prefix(self: "AstBuildPass", node: ast.AstNode) -> None:
        """No action needed, absorbed by parent."""

    def exit_import_path_tail(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) > 2:
            node.kid = node.kid[0].kid + [node.kid[1], node.kid[2]]

    def exit_name_as_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build MOD_ITEM list of Ast nodes. TODO: VALIDATE."""
        meta = {}
        meta["alias"] = ast.Blank()
        if node.kid[0].name == "NAME":
            meta["name"] = node.kid[0]
            node.parent.kid = [node] + node.parent.kid
            if len(node.kid) == 3:
                node.kid = [node.kid[0], node.kid[2]]
                meta["alias"] = node.kid[1]
            else:
                node.kid = [node.kid[0]]
        elif node.kid[-2].name == "KW_AS":
            node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
            node.kid = [node.kid[-3], node.kid[-1]]
            meta["name"] = node.kid[-3]
            meta["alias"] = node.kid[-1]
        else:
            node.parent.kid = [node] + node.kid[:-3] + node.parent.kid
            node.kid = [node.kid[-1]]
            meta["name"] = node.kid[-1]
        update_kind(node, ast.ModuleItem, **meta)

    def exit_architype(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Replace self with kid."""
        replace_node(node, node.kid[0])

    def exit_architype_inline_spec(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build various architype Ast nodes."""
        meta = {
            "doc": node.kid[0],
            "typ": node.kid[1],
            "access": node.kid[2],
            "name": node.kid[3],
            "base_classes": node.kid[4],
            "body": node.kid[5],
        }
        update_kind(node, ast.Architype, **meta)

    def exit_architype_decl(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ArchDecl Ast node."""
        del node.kid[-1]
        update_kind(
            node,
            ast.ArchDecl,
            doc=node.kid[0],
            typ=node.kid[1],
            access=node.kid[2],
            name=node.kid[3],
            base_classes=node.kid[4],
        )

    def exit_architype_def(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ArchDef Ast node."""
        update_kind(
            node,
            ast.ArchDef,
            doc=node.kid[0],
            mod=node.kid[1] if len(node.kid) == 4 else ast.Blank(),
            arch=node.kid[2] if len(node.kid) == 4 else node.kid[1],
            body=node.kid[-1],
        )

    def exit_inherited_archs(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        if type(node.kid[0]) == ast.Blank:
            del node.kid[0]
        update_kind(node, ast.BaseClasses, base_classes=node.kid)

    def exit_sub_name(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build SUB_NAME Ast node."""
        replace_node(node, node.kid[1])

    def exit_ability(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Ability Ast node."""
        replace_node(node, node.kid[0])

    def exit_ability_inline_spec(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build various ability Ast nodes."""
        del node.kid[1]
        meta = {
            "doc": node.kid[0],
            "access": node.kid[1],
            "name": node.kid[2],
            "body": node.kid[-1],
            "signature": node.kid[-2],
            "is_func": False,
        }
        if type(node.kid[-2]) == ast.FuncSignature:
            meta["is_func"] = True
        update_kind(node, ast.Ability, **meta)

    def exit_ability_decl(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AbilityDecl Ast node."""
        del node.kid[1]
        del node.kid[-1]
        meta = {
            "doc": node.kid[0],
            "access": node.kid[1],
            "name": node.kid[2],
            "signature": node.kid[3],
            "is_func": False,
        }
        if type(node.kid[-1]) == ast.FuncSignature:
            meta["is_func"] = True
        update_kind(node, ast.AbilityDecl, **meta)

    def exit_ability_def(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AbilityDef Ast node."""
        update_kind(
            node,
            ast.AbilityDef,
            doc=node.kid[0],
            mod=node.kid[1] if len(node.kid) == 4 else ast.Blank(),
            ability=node.kid[2] if len(node.kid) == 4 else node.kid[1],
            body=node.kid[-1],
        )

    def exit_sub_ability_spec(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AbilitySpec Ast node."""
        meta = {"doc": node.kid[0]}
        if node.kid[1].name == "NAME":
            meta["mod"] = node.kid[1]
            meta["arch"] = node.kid[2]
            meta["name"] = node.kid[3]
            if type(node.kid[4]) == ast.FuncSignature:
                meta["signature"] = node.kid[4]
                meta["body"] = node.kid[5]
            else:
                meta["signature"] = ast.Blank()
                meta["body"] = node.kid[4]
        else:
            meta["mod"] = ast.Blank()
            meta["arch"] = node.kid[1]
            meta["name"] = node.kid[2]
            if type(node.kid[3]) == ast.FuncSignature:
                meta["signature"] = node.kid[3]
                meta["body"] = node.kid[4]
            else:
                meta["signature"] = ast.Blank()
                meta["body"] = node.kid[3]
        update_kind(node, ast.AbilitySpec, **meta)

    def exit_member_block(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ARCH_BLOCK Ast node."""
        if len(node.kid) == 3:
            node = replace_node(node, node.kid[1])
        else:
            node.kid = []
        update_kind(node, ast.ArchBlock, members=node.kid)

    def exit_member_stmt_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]

    def exit_member_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Replace self with actual attr stmt."""
        node = replace_node(node, node.kid[0])

    def exit_has_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Move var list up to parent."""
        node.kid = [node.kid[0], node.kid[2], node.kid[3]]
        update_kind(
            node, ast.ArchHas, doc=node.kid[0], access=node.kid[1], vars=node.kid[2]
        )

    def exit_has_assign_clause(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Push list of individual vars into parent."""
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        update_kind(node, ast.HasVarList, vars=node.kid)

    def exit_typed_has_clause(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build HasVar Ast node."""
        if len(node.kid) == 4:
            del node.kid[2]
        update_kind(
            node,
            ast.HasVar,
            name=node.kid[0],
            type_tag=node.kid[1],
            value=node.kid[2] if len(node.kid) == 3 else ast.Blank(),
        )

    def exit_type_tag(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build TypeSpec Ast node."""
        replace_node(node, node.kid[1])

    def exit_return_type_tag(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ReturnTypeSpec Ast node."""
        if len(node.kid) == 2:
            replace_node(node, node.kid[1])
        else:
            replace_node(node, ast.Blank())

    def exit_type_name(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build TypeName Ast node."""
        meta = {"typ": node.kid[0], "nested1": ast.Blank(), "nested2": ast.Blank()}
        if len(node.kid) == 4:
            node.kid = [node.kid[0], node.kid[2]]
            meta["nested1"] = node.kid[1]
        elif len(node.kid) == 6:
            node.kid = [node.kid[0], node.kid[2], node.kid[4]]
            meta["nested1"] = node.kid[1]
            meta["nested2"] = node.kid[2]
        update_kind(node, ast.TypeSpec, **meta)

    def exit_builtin_type(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build BuiltinType Ast node."""
        replace_node(node, node.kid[0])

    def exit_can_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build CanStmt Ast node."""
        replace_node(node, node.kid[0])

    def exit_can_ds_ability(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Data spatial can Ast node."""
        del node.kid[1]
        if type(node.kid[-1]) == ast.Token and node.kid[-1].name == "SEMI":
            del node.kid[-1]
            update_kind(
                node,
                ast.ArchCanDecl,
                doc=node.kid[0],
                access=node.kid[1],
                name=node.kid[2],
                signature=node.kid[3],
            )
        else:
            update_kind(
                node,
                ast.ArchCan,
                doc=node.kid[0],
                access=node.kid[1],
                name=node.kid[2],
                signature=node.kid[3],
                body=node.kid[4],
            )

    def exit_can_func_ability(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Function can Ast node."""
        self.exit_can_ds_ability(node)

    def exit_event_clause(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build EventClause Ast node."""
        if len(node.kid) == 1:
            make_blank(node)
        elif len(node.kid) == 2:
            node.kid = [node.kid[1]]
            update_kind(
                node, ast.EventSignature, event=node.kid[0], arch_tag_info=ast.Blank()
            )
        else:
            node.kid = [node.kid[1], node.kid[2]]
            update_kind(
                node, ast.EventSignature, event=node.kid[1], arch_tag_info=node.kid[0]
            )

    def exit_name_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build NameList Ast node."""
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        update_kind(node, ast.NameList, names=node.kid)

    def exit_func_decl(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build FuncDecl Ast node."""
        if len(node.kid) == 3:
            node.kid = [node.kid[-1]]
            update_kind(
                node, ast.FuncSignature, params=ast.Blank(), return_type=node.kid[0]
            )
        else:
            node.kid = [node.kid[1], node.kid[3]]
            update_kind(
                node, ast.FuncSignature, params=node.kid[0], return_type=node.kid[1]
            )

    def exit_func_decl_param_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build FuncDeclParamList Ast node."""
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        update_kind(node, ast.FuncParams, params=node.kid)

    def exit_param_var(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ParamVar Ast node."""
        if len(node.kid) == 4:
            del node.kid[2]
        update_kind(
            node,
            ast.ParamVar,
            name=node.kid[0],
            type_tag=node.kid[1],
            value=node.kid[2] if len(node.kid) == 3 else ast.Blank(),
        )

    def exit_code_block(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build CodeBlock Ast node."""
        if len(node.kid) == 3:
            node = replace_node(node, node.kid[1])
        else:
            node.kid = []
        update_kind(node, ast.CodeBlock, stmts=node.kid)

    def exit_statement_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build StatementList Ast node."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]

    def exit_statement(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Statement Ast node."""
        replace_node(node, node.kid[0])

    def exit_if_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build IfStmt Ast node."""
        if len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            update_kind(
                node,
                ast.IfStmt,
                condition=node.kid[0],
                body=node.kid[1],
                elseifs=ast.Blank(),
                else_body=ast.Blank(),
            )
        elif len(node.kid) == 4 and type(node.kid[3]) == ast.ElseIfs:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            update_kind(
                node,
                ast.IfStmt,
                condition=node.kid[0],
                body=node.kid[1],
                elseifs=node.kid[2],
                else_body=ast.Blank(),
            )
        elif len(node.kid) == 4:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            update_kind(
                node,
                ast.IfStmt,
                condition=node.kid[0],
                body=node.kid[1],
                elseifs=ast.Blank(),
                else_body=node.kid[2],
            )
        else:
            node.kid = [node.kid[1], node.kid[2], node.kid[3], node.kid[4]]
            update_kind(
                node,
                ast.IfStmt,
                condition=node.kid[0],
                body=node.kid[1],
                elseifs=node.kid[2],
                else_body=node.kid[3],
            )

    def exit_elif_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ElifStmtList Ast node."""
        cpy_node = copy(node)
        cpy_node.kid = [node.kid[-2], node.kid[-1]]
        cpy_node = convert_kind(  # coverts ElseIf to IfStmt for ElseIfs list
            cpy_node,
            ast.IfStmt,
            condition=cpy_node.kid[0],
            body=cpy_node.kid[1],
            elseifs=ast.Blank(),
            else_body=ast.Blank(),
        )
        if len(node.kid) == 3:
            node.kid = [cpy_node]
        if len(node.kid) == 4:
            node.kid = node.kid[0].kid + [cpy_node]
        update_kind(node, ast.ElseIfs, elseifs=node.kid)

    def exit_else_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ElseStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.ElseStmt, body=node.kid[0])

    def exit_try_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build TryStmt Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[1]]
            update_kind(
                node,
                ast.TryStmt,
                body=node.kid[0],
                excepts=ast.Blank(),
                finally_body=ast.Blank(),
            )
        elif len(node.kid) == 3 and type(node.kid[2]) == ast.ExceptList:
            node.kid = [node.kid[1], node.kid[2]]
            update_kind(
                node,
                ast.TryStmt,
                body=node.kid[0],
                excepts=node.kid[1],
                finally_body=ast.Blank(),
            )
        elif len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            update_kind(
                node,
                ast.TryStmt,
                body=node.kid[0],
                excepts=ast.Blank(),
                finally_body=node.kid[1],
            )
        else:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            update_kind(
                node,
                ast.TryStmt,
                body=node.kid[0],
                excepts=node.kid[1],
                finally_body=node.kid[2],
            )

    def exit_except_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ExceptList Ast node."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        update_kind(node, ast.ExceptList, excepts=node.kid)

    def exit_except_def(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ExceptDef Ast node."""
        if len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            update_kind(
                node, ast.Except, typ=node.kid[0], name=ast.Blank(), body=node.kid[1]
            )
        else:
            node.kid = [node.kid[1], node.kid[3], node.kid[4]]
            update_kind(
                node, ast.Except, typ=node.kid[0], name=node.kid[1], body=node.kid[2]
            )

    def exit_finally_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build FinallyStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.FinallyStmt, body=node.kid[0])

    def exit_for_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ForStmt Ast node."""
        if node.kid[2].name == "KW_TO":
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[6]]
            update_kind(
                node,
                ast.IterForStmt,
                iter=node.kid[0],
                condition=node.kid[1],
                count_by=node.kid[2],
                body=node.kid[3],
            )
        elif node.kid[2].name == "KW_IN":
            node.kid = [node.kid[1], node.kid[3], node.kid[4]]
            update_kind(
                node,
                ast.InForStmt,
                name=node.kid[0],
                collection=node.kid[1],
                body=node.kid[2],
            )
        else:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[6]]
            update_kind(
                node,
                ast.DictForStmt,
                k_name=node.kid[0],
                v_name=node.kid[1],
                collection=node.kid[2],
                body=node.kid[3],
            )

    def exit_while_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build WhileStmt Ast node."""
        node.kid = [node.kid[1], node.kid[2]]
        update_kind(node, ast.WhileStmt, condition=node.kid[0], body=node.kid[1])

    def exit_raise_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build RaiseStmt Ast node."""
        if len(node.kid) == 1:
            node.kid = []
            update_kind(node, ast.RaiseStmt, cause=ast.Blank())
        else:
            node.kid = [node.kid[1]]
            update_kind(node, ast.RaiseStmt, cause=node.kid[0])

    def exit_assert_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AssertStmt Ast node."""
        if len(node.kid) == 4:
            node.kid = [node.kid[1], node.kid[3]]
            update_kind(
                node, ast.AssertStmt, condition=node.kid[0], error_msg=node.kid[1]
            )
        else:
            node.kid = [node.kid[1]]
            update_kind(node, ast.AssertStmt, condition=node.kid[0])

    def exit_ctrl_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build CtrlStmt Ast node."""
        update_kind(node, ast.CtrlStmt, stmt=node.kid[0])

    def exit_delete_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build DeleteStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.DeleteStmt, target=node.kid[0])

    def exit_report_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ReportStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.ReportStmt, expr=node.kid[0])

    def exit_return_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ReturnStmt Ast node."""
        if len(node.kid) == 1:
            node.kid = []
            update_kind(node, ast.ReturnStmt, expr=ast.Blank())
        else:
            node.kid = [node.kid[1]]
            update_kind(node, ast.ReturnStmt, expr=node.kid[0])

    def exit_walker_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build WalkerStmt Ast node."""
        replace_node(node, node.kid[1])

    def exit_ignore_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build IgnoreStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.IgnoreStmt, target=node.kid[0])

    def exit_visit_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build VisitStmt Ast node."""
        meta = {"typ": ast.Blank(), "else_body": ast.Blank()}
        if node.kid[-1].name == "SEMI":
            if len(node.kid) == 4:
                node.kid = [node.kid[1], node.kid[2]]
                meta["typ"] = node.kid[0]
                meta["target"] = node.kid[1]
            else:
                node.kid = [node.kid[1]]
                meta["target"] = node.kid[0]
        elif len(node.kid) == 4:
            node.kid = [node.kid[1], node.kid[2], node.kid[3]]
            meta["typ"] = node.kid[0]
            meta["target"] = node.kid[1]
            meta["else_body"] = node.kid[2]
        else:
            node.kid = [node.kid[1], node.kid[2]]
            meta["target"] = node.kid[0]
            meta["else_body"] = node.kid[1]
        update_kind(node, ast.VisitStmt, **meta)

    def exit_revisit_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build RevisitStmt Ast node."""
        meta = {"hops": ast.Blank(), "else_body": ast.Blank()}
        if node.kid[-1].name == "SEMI":
            if len(node.kid) == 3:
                node.kid = [node.kid[1]]
                meta["hops"] = node.kid[0]
        elif len(node.kid) == 3:
            node.kid = [node.kid[1], node.kid[2]]
            meta["hops"] = node.kid[0]
            meta["else_body"] = node.kid[1]
        else:
            node.kid = [node.kid[1], node.kid[2]]
            meta["hops"] = node.kid[0]
            meta["else_body"] = node.kid[1]
        update_kind(node, ast.RevisitStmt, **meta)

    def exit_disengage_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build DisengageStmt Ast node."""
        node.kid = []
        update_kind(node, ast.DisengageStmt)

    def exit_yield_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build YieldStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.YieldStmt, expr=node.kid[0])

    def exit_sync_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build SyncStmt Ast node."""
        node.kid = [node.kid[1]]
        update_kind(node, ast.SyncStmt, target=node.kid[0])

    def exit_assignment(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Assignment Ast node."""
        node.kid = [node.kid[-3], node.kid[-1]]
        update_kind(
            node, ast.Assignment, is_static=False, target=node.kid[0], value=node.kid[1]
        )

    def exit_static_assignment(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build StaticAssignment Ast node."""
        node = replace_node(node, node.kid[1])
        for i in node.kid:
            i.is_static = True

    def binary_op_helper(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Reused as utility function for binary operators."""
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            node.kid = [node.kid[0], node.kid[1], node.kid[2]]
            update_kind(
                node,
                ast.BinaryExpr,
                left=node.kid[0],
                op=node.kid[1],
                right=node.kid[2],
            )

    def exit_expression(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Expression Ast node."""
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            node.kid = [node.kid[0], node.kid[1], node.kid[2]]
            update_kind(
                node,
                ast.IfElseExpr,
                value=node.kid[0],
                condition=node.kid[1],
                else_value=node.kid[2],
            )

    def exit_walrus_assign(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build WalrusAssign Ast node."""
        self.binary_op_helper(node)

    def exit_pipe(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Pipe Ast node."""
        self.binary_op_helper(node)

    def exit_pipe_back(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build PipeBack Ast node."""
        self.binary_op_helper(node)

    def exit_elvis_check(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ElvisCheck Ast node."""
        self.binary_op_helper(node)

    def exit_logical(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Logical Ast node."""
        self.binary_op_helper(node)

    def exit_compare(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Compare Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            update_kind(node, ast.UnaryExpr, op=node.kid[0], operand=node.kid[1])
        else:
            self.binary_op_helper(node)

    def exit_arithmetic(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Arithmetic Ast node."""
        self.binary_op_helper(node)

    def exit_term(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Term Ast node."""
        self.binary_op_helper(node)

    def exit_factor(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Factor Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            update_kind(node, ast.UnaryExpr, op=node.kid[0], operand=node.kid[1])
        else:
            self.binary_op_helper(node)

    def exit_power(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Power Ast node."""
        self.binary_op_helper(node)

    def exit_connect(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Connect Ast node."""
        self.binary_op_helper(node)

    def exit_spawn_object(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build SpawnObjectExpr Ast node."""
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            node.kid = [node.kid[1]]
            update_kind(node, ast.SpawnObjectExpr, target=node.kid[0])

    def exit_unpack(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Unpack Ast node."""
        if len(node.kid) == 1:
            replace_node(node, node.kid[0])
        else:
            node.kid = [node.kid[-1]]
            if len(node.kid) == 2:
                update_kind(node, ast.UnpackExpr, target=node.kid[0], is_dict=False)
            else:
                update_kind(node, ast.UnpackExpr, target=node.kid[0], is_dict=True)

    def exit_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Ref Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            update_kind(node, ast.UnaryExpr, op=node.kid[0], operand=node.kid[1])
        else:
            self.binary_op_helper(node)

    def exit_ds_call(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build DSCall Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[0], node.kid[1]]
            update_kind(node, ast.UnaryExpr, op=node.kid[0], operand=node.kid[1])
        else:
            self.binary_op_helper(node)

    def exit_walrus_op(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Replace self with child."""
        replace_node(node, node.kid[0])

    def exit_cmp_op(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build CmpOp Ast node."""
        replace_node(node, node.kid[0])

    def exit_spawn_op(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build SpawnOp Ast node."""
        replace_node(node, node.kid[0])

    def exit_atom(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Atom Ast node."""
        if len(node.kid) == 3:
            replace_node(node, node.kid[1])
        else:
            replace_node(node, node.kid[0])

    def exit_atom_literal(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AtomLiteral Ast node."""
        replace_node(node, node.kid[0])

    def exit_atom_collection(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AtomCollection Ast node."""
        replace_node(node, node.kid[0])

    def exit_multistring(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Multistring Ast node."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        update_kind(node, ast.MultiString, strings=node.kid)

    def exit_list_val(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ListVal Ast node."""
        if len(node.kid) > 2:
            node = replace_node(node, node.kid[1])
        else:
            node.kid = []
        update_kind(node, ast.ListVal, values=node.kid)

    def exit_expr_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ExprList Ast node."""
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        update_kind(node, ast.ExprList, values=node.kid)

    def exit_dict_val(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build DictVal Ast node."""
        if len(node.kid) == 3:
            node.kid = node.kid[:-3]
        else:
            node.kid = []
        update_kind(node, ast.DictVal, kv_pairs=node.kid)

    def exit_comprehension(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Comprehension Ast node."""
        meta = {
            "key_expr": ast.Blank(),
            "out_expr": ast.Blank(),
            "name": ast.Blank(),
            "collection": ast.Blank(),
            "conditional": ast.Blank(),
        }
        if node.kid[2].name == "COLON":
            meta["key_expr"] = node.kid[1]
            meta["out_expr"] = node.kid[3]
            meta["name"] = node.kid[5]
            meta["collection"] = node.kid[7]
        else:
            meta["out_expr"] = node.kid[1]
            meta["name"] = node.kid[3]
            meta["collection"] = node.kid[5]
        if node.kid[-3].name == "KW_IF":
            meta["conditional"] = node.kid[-2]
        if len(node.kid) == 7:
            node.kid = [node.kid[1], node.kid[3], node.kid[5]]
        elif len(node.kid) == 9:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[7]]
        elif len(node.kid) == 11:
            node.kid = [node.kid[1], node.kid[3], node.kid[5], node.kid[7], node.kid[9]]
        update_kind(node, ast.Comprehension, **meta)

    def exit_kv_pairs(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build KVPairs Ast node."""
        if len(node.kid) == 3:
            node.parent.kid = [node] + node.parent.kid
            node.kid = [node.kid[0], node.kid[2]]
        else:
            node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
            node.kid = [node.kid[-3], node.kid[-1]]
        update_kind(node, ast.KVPair, key=node.kid[0], value=node.kid[1])

    def exit_atomic_chain(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AtomicChain Ast node."""
        replace_node(node, node.kid[0])

    def exit_atomic_chain_unsafe(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AtomicChain Ast node."""
        if len(node.kid) == 3:
            del node.kid[1]
        replace_node(
            node,
            ast.AtomTrailer(
                target=node.kid[0],
                right=node.kid[1],
                null_ok=False,
                parent=node.parent,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_atomic_chain_safe(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AtomicChain with safety Ast node."""
        del node.kid[1]
        if len(node.kid) == 3:
            del node.kid[1]
        update_kind(
            node, ast.AtomTrailer, target=node.kid[0], right=node.kid[1], null_ok=True
        )

    def exit_atomic_call(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Call Ast node."""
        update_kind(node, ast.FuncCall, target=node.kid[0], params=node.kid[1])

    def exit_func_call_tail(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build FuncCall Ast node."""
        if len(node.kid) == 2:
            replace_node(node, ast.Blank())
        else:
            replace_node(node, node.kid[1])

    def exit_param_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ParamList Ast node."""
        if len(node.kid) == 1:
            if type(node.kid[0]) == ast.ExprList:
                update_kind(
                    node, ast.ParamList, p_args=node.kid[0], p_kwargs=ast.Blank()
                )
            else:
                update_kind(
                    node, ast.ParamList, p_args=ast.Blank(), p_kwargs=node.kid[0]
                )
        else:
            update_kind(node, ast.ParamList, p_args=node.kid[0], p_kwargs=node.kid[1])

    def exit_assignment_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AssignmentList Ast node."""
        if len(node.kid) == 3:
            node.kid = node.kid[0].kid + [node.kid[2]]
        update_kind(node, ast.AssignmentList, values=node.kid)

    def exit_index_slice(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build IndexSlice Ast node."""
        if len(node.kid) == 3:
            node.kid = node.kid[1]
            update_kind(node, ast.IndexSlice, start=node.kid[0], stop=ast.Blank())
        else:
            node.kid = [node.kid[1], node.kid[3]]
            update_kind(node, ast.IndexSlice, start=node.kid[0], stop=node.kid[1])

    def exit_global_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build GlobalRef Ast node."""
        node.kid = [node.kid[-1]]
        update_kind(node, ast.GlobalRef, name=node.kid[-1])

    def exit_here_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build GlobalRef Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[-1]]
            update_kind(node, ast.HereRef, name=node.kid[-1])
        else:
            node.kid = []
            update_kind(node, ast.HereRef, name=ast.Blank())

    def exit_visitor_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build GlobalRef Ast node."""
        if len(node.kid) == 2:
            node.kid = [node.kid[-1]]
            update_kind(node, ast.VisitorRef, name=node.kid[-1])
        else:
            node.kid = []
            update_kind(node, ast.VisitorRef, name=ast.Blank())

    def exit_arch_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ArchRef Ast node."""
        replace_node(node, node.kid[0])

    def exit_strict_arch_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build strict ArchRef Ast node."""
        replace_node(node, node.kid[0])

    def exit_node_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build NodeRef Ast node."""
        node.kid = [node.kid[-1]]
        update_kind(node, ast.NodeRef, name=node.kid[-1])

    def exit_edge_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build EdgeRef Ast node."""
        node.kid = [node.kid[-1]]
        update_kind(node, ast.EdgeRef, name=node.kid[-1])

    def exit_walker_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build WalkerRef Ast node."""
        node.kid = [node.kid[-1]]
        update_kind(node, ast.WalkerRef, name=node.kid[-1])

    def exit_object_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ObjectRef Ast node."""
        node.kid = [node.kid[-1]]
        update_kind(node, ast.ObjectRef, name=node.kid[-1])

    def exit_ability_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AbilityRef Ast node."""
        node.kid = [node.kid[-1]]
        update_kind(node, ast.AbilityRef, name=node.kid[-1])

    def exit_edge_op_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build EdgeOpRef Ast node."""
        replace_node(node, node.kid[0])

    def exit_edge_to(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build EdgeTo Ast node."""
        if len(node.kid) == 3:
            update_kind(
                node, ast.EdgeOpRef, filter_cond=node.kid[1], edge_dir=ast.EdgeDir.OUT
            )
        else:
            update_kind(
                node, ast.EdgeOpRef, filter_cond=ast.Blank(), edge_dir=ast.EdgeDir.OUT
            )

    def exit_edge_from(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build EdgeFrom Ast node."""
        if len(node.kid) == 3:
            update_kind(
                node, ast.EdgeOpRef, filter_cond=node.kid[1], edge_dir=ast.EdgeDir.IN
            )
        else:
            update_kind(
                node, ast.EdgeOpRef, filter_cond=ast.Blank(), edge_dir=ast.EdgeDir.IN
            )

    def exit_edge_any(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build EdgeAny Ast node."""
        if len(node.kid) == 3:
            update_kind(
                node, ast.EdgeOpRef, filter_cond=node.kid[1], edge_dir=ast.EdgeDir.BOTH
            )
        else:
            update_kind(
                node, ast.EdgeOpRef, filter_cond=ast.Blank(), edge_dir=ast.EdgeDir.BOTH
            )

    def exit_connect_op(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ConnectOp Ast node."""
        replace_node(node, node.kid[0])

    def exit_disconnect_op(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build DisconnectOp Ast node."""
        node = replace_node(node, node.kid[1])
        node = replace_node(
            node,
            ast.DisconnectOp(
                filter_cond=node.filter_cond,
                edge_dir=node.edge_dir,
                parent=node.parent,
                kid=node.kid,
                line=node.line,
            ),
        )

    def exit_connect_to(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ConnectTo Ast node."""
        if len(node.kid) == 3:
            update_kind(
                node, ast.ConnectOp, spawn=node.kid[1], edge_dir=ast.EdgeDir.OUT
            )
        else:
            update_kind(
                node, ast.ConnectOp, spawn=ast.Blank(), edge_dir=ast.EdgeDir.OUT
            )

    def exit_connect_from(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ConnectFrom Ast node."""
        if len(node.kid) == 3:
            update_kind(node, ast.ConnectOp, spawn=node.kid[1], edge_dir=ast.EdgeDir.IN)
        else:
            update_kind(node, ast.ConnectOp, spawn=ast.Blank(), edge_dir=ast.EdgeDir.IN)

    def exit_connect_any(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ConnectAny Ast node."""
        if len(node.kid) == 3:
            update_kind(
                node, ast.ConnectOp, spawn=node.kid[1], edge_dir=ast.EdgeDir.BOTH
            )
        else:
            update_kind(
                node, ast.ConnectOp, spawn=ast.Blank(), edge_dir=ast.EdgeDir.BOTH
            )

    def exit_filter_ctx(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build FilterCtx Ast node."""
        node.kid = node.kid[:-4]
        update_kind(node, ast.FilterCtx, compares=node.kid)

    def exit_spawn_ctx(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build SpawnCtx Ast node."""
        node = replace_node(node, node.kid[1])
        update_kind(node, ast.SpawnCtx, spawns=node.kid)

    def exit_filter_compare_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build FilterCompareList Ast node."""
        if len(node.kid) == 3:
            node.parent.kid = [node] + node.parent.kid
        else:
            node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
            node.kid = [node.kid[-3], node.kid[-2], node.kid[-1]]
        update_kind(
            node, ast.BinaryExpr, op=node.kid[1], left=node.kid[0], right=node.kid[2]
        )

    def exit_empty(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build Empty Ast node."""
        make_blank(node)
