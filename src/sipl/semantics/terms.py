"""Recursive semantic-term construction in the course ASIPL notation."""

from dataclasses import dataclass

from sipl.ast import (
    Assignment,
    BinaryExpression,
    Block,
    Comparison,
    IfStatement,
    IntegerLiteral,
    LogicalNot,
    LogicalOr,
    Node,
    Program,
    Sequence,
    Skip,
    SourceSpan,
    UnaryMinus,
    Variable,
    WhileStatement,
)


@dataclass(frozen=True)
class SemanticTerm:
    """A typed algebraic term, not a value computed from a state."""

    symbol: str
    arguments: tuple["SemanticTerm", ...] = ()
    value: str | int | None = None
    span: SourceSpan | None = None


def build_term(node: Node) -> SemanticTerm:
    """Translate a SIPL AST recursively using the course rules."""

    def term(
        symbol: str,
        *args: SemanticTerm,
        value=None,
    ) -> SemanticTerm:
        return SemanticTerm(
            symbol=symbol,
            arguments=tuple(args),
            value=value,
            span=node.span,
        )

    # Program: NS_Prog
    if isinstance(node, Program):
        return build_term(node.body)

    # begin/end: NS_Stm_BE
    if isinstance(node, Block):
        return build_term(node.body)

    # Sequential composition: NS_Stm_Seq
    if isinstance(node, Sequence):
        elements = [
            build_term(statement)
            for statement in node.statements
        ]

        if not elements:
            raise ValueError(
                "Empty SIPL statement sequence"
            )

        result = elements[0]

        for next_term in elements[1:]:
            result = term(
                "SEQ",
                result,
                next_term,
            )

        return result

    # Assignment: NS_Stm_As
    if isinstance(node, Assignment):
        return term(
            "AS",
            build_term(node.value),
            value=node.name,
        )

    # Conditional: NS_Stm_If
    if isinstance(node, IfStatement):
        return term(
            "IF",
            build_term(node.condition),
            build_term(node.then_branch),
            build_term(node.else_branch),
        )

    # While loop: NS_Stm_Wh
    if isinstance(node, WhileStatement):
        return term(
            "WH",
            build_term(node.condition),
            build_term(node.body),
        )

    # Skip: NS_Stm_Skip
    if isinstance(node, Skip):
        return term("id")

    # Numeric literal: NS_A_Num
    if isinstance(node, IntegerLiteral):
        return term(
            "num",
            value=node.value,
        )

    # Variable: NS_A_Var
    if isinstance(node, Variable):
        return term(
            "var",
            value=node.name,
        )

    # Unary minus is an extension of the base rules.
    if isinstance(node, UnaryMinus):
        return term(
            "S1",
            build_term(node.operand),
            value="uminus",
        )

    # Arithmetic: NS_A_Add / NS_A_Sub / NS_A_Mult
    if isinstance(node, BinaryExpression):
        names = {
            "+": "add",
            "-": "sub",
            "*": "mult",
        }

        if node.operator not in names:
            raise ValueError(
                "Unsupported SIPL arithmetic operator: "
                f"{node.operator}"
            )

        return term(
            "S2",
            build_term(node.left),
            build_term(node.right),
            value=names[node.operator],
        )

    # Comparisons: NS_B_eq / NS_B_gr
    if isinstance(node, Comparison):
        names = {
            "=": "eq",
            ">": "gr",
        }

        if node.operator not in names:
            raise ValueError(
                "Unsupported SIPL comparison: "
                f"{node.operator}"
            )

        return term(
            "S2",
            build_term(node.left),
            build_term(node.right),
            value=names[node.operator],
        )

    # Logical OR: NS_B_or
    if isinstance(node, LogicalOr):
        return term(
            "S2",
            build_term(node.left),
            build_term(node.right),
            value="or",
        )

    # Logical NOT: NS_B_neg
    if isinstance(node, LogicalNot):
        return term(
            "S1",
            build_term(node.operand),
            value="neg",
        )

    raise TypeError(
        f"Unsupported AST node: {type(node).__name__}"
    )


def format_term(term: SemanticTerm) -> str:
    """Render an ASIPL semantic term using course notation."""

    if term.symbol == "num":
        return "".join(
            character + "\u0305"
            for character in str(term.value)
        )

    if term.symbol == "var":
        return f"{term.value}⇒"

    if term.symbol == "id":
        return "id"

    if term.symbol == "SEQ":
        return (
            f"{format_term(term.arguments[0])}"
            " · "
            f"{format_term(term.arguments[1])}"
        )

    if term.symbol == "AS":
        return (
            f"AS^{term.value}("
            f"{format_term(term.arguments[0])})"
        )

    if term.symbol in ("S1", "S2"):
        marker = (
            "S¹"
            if term.symbol == "S1"
            else "S²"
        )

        arguments = ", ".join(
            format_term(argument)
            for argument in term.arguments
        )

        return (
            f"{marker}("
            f"{term.value}, {arguments})"
        )

    if term.symbol in ("IF", "WH"):
        arguments = ", ".join(
            format_term(argument)
            for argument in term.arguments
        )

        return f"{term.symbol}({arguments})"

    raise ValueError(
        f"Unknown semantic operator: {term.symbol}"
    )


def term_to_data(term: SemanticTerm) -> dict:
    """Serialize the semantic term with source coordinates."""

    span = term.span

    return {
        "symbol": term.symbol,
        "value": term.value,
        "span": (
            None
            if span is None
            else {
                "start_line": span.start_line,
                "start_column": span.start_column,
                "end_line": span.end_line,
                "end_column": span.end_column,
                "start_pos": span.start_pos,
                "end_pos": span.end_pos,
            }
        ),
        "arguments": [
            term_to_data(argument)
            for argument in term.arguments
        ],
    }
