"""Lexer for Jac language."""

from jaseci.utils.sly.lex import Lexer, Token


class JacLexer(Lexer):
    """Jac Lexer."""

    tokens = {
        "FLOAT",
        "STRING",
        "DOC_STRING",
        "FSTRING",
        "BOOL",
        "INT",
        "NULL",
        "NAME",
        "TYP_STRING",
        "TYP_INT",
        "TYP_FLOAT",
        "TYP_LIST",
        "TYP_TUPLE",
        "TYP_SET",
        "TYP_DICT",
        "TYP_BOOL",
        "TYP_BYTES",
        "KW_OBJECT",
        "KW_TYPE",
        "KW_NODE",
        "KW_IGNORE",
        "KW_VISITOR",
        "KW_VISIT",
        "KW_REVISIT",
        "KW_SPAWN",
        "KW_WITH",
        "KW_ENTRY",
        "KW_EXIT",
        "KW_CONTEXT",
        "KW_HERE",
        "KW_INFO",
        "KW_DETAILS",
        "KW_IMPORT",
        "KW_FROM",
        "KW_AS",
        "KW_EDGE",
        "KW_WALKER",
        "KW_ABILITY",
        "KW_ASYNC",
        "KW_SYNC",
        "KW_TEST",
        "KW_ASSERT",
        "COLON",
        "DBL_COLON",
        "PIPE_FWD",
        "LBRACE",
        "RBRACE",
        "SEMI",
        "EQ",
        "ADD_EQ",
        "SUB_EQ",
        "MUL_EQ",
        "DIV_EQ",
        "WALRUS_EQ",
        "KW_AND",
        "KW_OR",
        "KW_IF",
        "KW_ELIF",
        "KW_ELSE",
        "KW_FOR",
        "KW_TO",
        "KW_BY",
        "KW_WHILE",
        "KW_CONTINUE",
        "KW_BREAK",
        "KW_DISENGAGE",
        "KW_YIELD",
        "KW_SKIP",
        "KW_REPORT",
        "KW_RETURN",
        "KW_DELETE",
        "KW_TRY",
        "KW_REF",
        "DOT",
        "NOT",
        "EE",
        "LT",
        "GT",
        "LTE",
        "GTE",
        "NE",
        "KW_IN",
        "KW_NIN",
        "KW_ANCHOR",
        "KW_HAS",
        "KW_GLOBAL",
        "KW_HIDDEN",
        "COMMA",
        "KW_CAN",
        "PLUS",
        "MINUS",
        "STAR_MUL",
        "DIV",
        "MOD",
        "POW",
        "LPAREN",
        "RPAREN",
        "LSQUARE",
        "RSQUARE",
        "ARROW_L",
        "ARROW_R",
        "ARROW_BI",
        "ARROW_L_p1",
        "ARROW_L_p2",
        "ARROW_R_p1",
        "ARROW_R_p2",
        "CARROW_L",
        "CARROW_R",
        "CARROW_BI",
        "CARROW_L_p1",
        "CARROW_L_p2",
        "CARROW_R_p1",
        "CARROW_R_p2",
        "GLOBAL_OP",
        "WALKER_OP",
        "NODE_OP",
        "OBJECT_OP",
        "SPAWN_OP",
        "NULL_OK",
    }

    # Ignored patterns
    ignore_ws = r"[ \t]+"
    ignore_newline = r"[\r\n]+"
    ignore_comment = r"/\*.*?\*/"
    ignore_line_comment = r"//.*"
    ignore_py_comment = r"#.*"

    # Regular expression rules for tokens
    FLOAT = r"(\d+)?\.\d+"
    DOC_STRING = r'"""[^"]*"""|\'\'\'[^\']*\'\'\''
    FSTRING = r'f"[^"\r\n]*"|f\'[^\'\r\n]*\''
    STRING = r'"[^"\r\n]*"|\'[^\'\r\n]*\''
    BOOL = r"True|False"
    KW_NIN = r"not in"
    INT = r"\d+"
    NULL = r"None"
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Keywords
    NAME["str"] = "TYP_STRING"
    NAME["int"] = "TYP_INT"
    NAME["float"] = "TYP_FLOAT"
    NAME["list"] = "TYP_LIST"
    NAME["tuple"] = "TYP_TUPLE"
    NAME["set"] = "TYP_SET"
    NAME["dict"] = "TYP_DICT"
    NAME["bool"] = "TYP_BOOL"
    NAME["bytes"] = "TYP_BYTES"
    NAME["object"] = "KW_OBJECT"
    NAME["type"] = "KW_TYPE"
    NAME["node"] = "KW_NODE"
    NAME["ignore"] = "KW_IGNORE"
    NAME["visitor"] = "KW_VISITOR"
    NAME["visit"] = "KW_VISIT"
    NAME["revisit"] = "KW_REVISIT"
    NAME["spawn"] = "KW_SPAWN"
    NAME["with"] = "KW_WITH"
    NAME["entry"] = "KW_ENTRY"
    NAME["exit"] = "KW_EXIT"
    NAME["context"] = "KW_CONTEXT"
    NAME["here"] = "KW_HERE"
    NAME["info"] = "KW_INFO"
    NAME["details"] = "KW_DETAILS"
    NAME["import"] = "KW_IMPORT"
    NAME["from"] = "KW_FROM"
    NAME["as"] = "KW_AS"
    NAME["edge"] = "KW_EDGE"
    NAME["walker"] = "KW_WALKER"
    NAME["ability"] = "KW_ABILITY"
    NAME["async"] = "KW_ASYNC"
    NAME["sync"] = "KW_SYNC"
    NAME["test"] = "KW_TEST"
    NAME["assert"] = "KW_ASSERT"
    NAME["and"] = "KW_AND"
    NAME["or"] = "KW_OR"
    NAME["if"] = "KW_IF"
    NAME["elif"] = "KW_ELIF"
    NAME["else"] = "KW_ELSE"
    NAME["for"] = "KW_FOR"
    NAME["to"] = "KW_TO"
    NAME["by"] = "KW_BY"
    NAME["while"] = "KW_WHILE"
    NAME["continue"] = "KW_CONTINUE"
    NAME["break"] = "KW_BREAK"
    NAME["disengage"] = "KW_DISENGAGE"
    NAME["yield"] = "KW_YIELD"
    NAME["skip"] = "KW_SKIP"
    NAME["report"] = "KW_REPORT"
    NAME["return"] = "KW_RETURN"
    NAME["del"] = "KW_DELETE"
    NAME["try"] = "KW_TRY"
    NAME["in"] = "KW_IN"
    NAME["not"] = "NOT"
    NAME["anchor"] = "KW_ANCHOR"
    NAME["has"] = "KW_HAS"
    NAME["global"] = "KW_GLOBAL"
    NAME["hidden"] = "KW_HIDDEN"
    NAME["can"] = "KW_CAN"

    # Special Arrow Tokens
    ARROW_L = r"<--"
    ARROW_R = r"-->"
    ARROW_BI = r"<-->"
    ARROW_L_p1 = r"<-\["
    ARROW_L_p2 = r"]-"
    ARROW_R_p1 = r"-\["
    ARROW_R_p2 = r"]->"
    CARROW_L = r"<\+\+"
    CARROW_R = r"\+\+>"
    CARROW_BI = r"<\+\+>"
    CARROW_L_p1 = r"<\+\["
    CARROW_L_p2 = r"]\+"
    CARROW_R_p1 = r"\+\["
    CARROW_R_p2 = r"]\+>"

    # Just special
    GLOBAL_OP = r":g:|:global:"
    WALKER_OP = r":w:|:walker:"
    NODE_OP = r":n:|:node:"
    OBJECT_OP = r":o:|:object:"
    SPAWN_OP = r"::>"
    NULL_OK = r"\?"

    # Token rules
    KW_AND = r"&&"
    KW_OR = r"\|\|"
    NOT = r"!"
    DBL_COLON = r"::"
    PIPE_FWD = r"\|>"
    COLON = r":"
    LBRACE = r"{"
    RBRACE = r"}"
    SEMI = r";"
    EE = r"=="
    EQ = r"="
    ADD_EQ = r"\+="
    SUB_EQ = r"-="
    MUL_EQ = r"\*="
    DIV_EQ = r"/="
    WALRUS_EQ = r":="
    KW_REF = r"&"
    DOT = r"\."
    LT = r"<"
    GT = r">"
    LTE = r"<="
    GTE = r">="
    NE = r"!="
    COMMA = r","
    PLUS = r"\+"
    MINUS = r"-"
    STAR_MUL = r"\*"
    DIV = r"/"
    MOD = r"%"
    POW = r"\^"
    LPAREN = r"\("
    RPAREN = r"\)"
    LSQUARE = r"\["
    RSQUARE = r"\]"

    def ignore_newline(self: "JacLexer", t: Token) -> Token:
        """Increment line number."""
        self.lineno += len(t.value)
        return t

    def DOC_STRING(self: "JacLexer", t: Token) -> Token:  # noqa: N802
        """Add docstring to lexer."""
        self.lineno += t.value.count("\n")
        self.lineno += t.value.count("\r")
        return t

    # Error handling rule
    def error(self: "JacLexer", t: Token) -> None:
        """Raise an error for illegal characters."""
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


class JacFStringLexer(Lexer):
    """Lexer for Jac f-strings."""

    tokens = {
        "DQ_L",
        "DQ_R",
        "MIDDLE",
        "SQ_L",
        "SQ_R",
        "FEXPR",
    }

    # Regular expression rules for f-strings pieces
    DQ_L = r'f"[^"{]*(?:{{[^"{]*)*{'  # Chomps "...{"
    DQ_R = r'}[^"}]*(?:}}[^"}]*)*"'  # Chomps "}..."
    MIDDLE = r'}[^"]*(?:{{[^"}]*}}[^"]*)*{'  # Chomps }...{
    SQ_L = r"f'[^'{]*(?:{{[^'{]*)*{"  # Chomps '...{'
    SQ_R = r"}[^'}]*(?:}}[^'}]*)*'"  # Chomps }...'

    FEXPR = r"[^{}]+"

    # Error handling rule
    def error(self: "JacLexer", t: Token) -> None:
        """Raise an error for illegal characters."""
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1