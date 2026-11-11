"""Conversion from Lark concrete syntax trees to the typed SIPL AST."""

from dataclasses import replace

from lark import Token, Tree

from sipl.ast import (
    Assignment,
    BinaryExpression,
    Block,
    Comparison,
    IfStatement,
    IntegerLiteral,
    LogicalNot,
    LogicalOr,
    Program,
    Sequence,
    Skip,
    SourceSpan,
    UnaryMinus,
    Variable,
    WhileStatement,
)
from sipl.syntax import parse_source


def _span(node: Tree | Token) -> SourceSpan:
    """Extract source coordinates from a Lark tree or token."""

    meta = node.meta if isinstance(node, Tree) else node

    return SourceSpan(
        start_line=meta.line,
        start_column=meta.column,
        end_line=meta.end_line,
        end_column=meta.end_column,
        start_pos=meta.start_pos,
        end_pos=meta.end_pos,
    )


def _build(node: Tree):
    """Recursively transform a Lark node into a SIPL AST node."""

    kind = node.data
    children = node.children
    span = _span(node)

    # Program

    if kind == "start":
        return Program(
            body=_build(children[0]),
            span=span,
        )

    # Statements

    if kind == "sequence":
        return Sequence(
            statements=tuple(
                _build(child)
                for child in children
            ),
            span=span,
        )

    if kind == "assignment":
        return Assignment(
            name=str(children[0]),
            value=_build(children[1]),
            span=span,
        )

    if kind == "conditional":
        return IfStatement(
            condition=_build(children[0]),
            then_branch=_build(children[1]),
            else_branch=_build(children[2]),
            span=span,
        )

    if kind == "loop":
        return WhileStatement(
            condition=_build(children[0]),
            body=_build(children[1]),
            span=span,
        )

    if kind == "block":
        return Block(
            body=_build(children[0]),
            span=span,
        )

    if kind == "skip_stmt":
        return Skip(span=span)

    # Arithmetic expressions

    if kind == "number":
        return IntegerLiteral(
            value=int(children[0]),
            span=span,
        )

    if kind == "variable":
        return Variable(
            name=str(children[0]),
            span=span,
        )

    if kind == "negative":
        return UnaryMinus(
            operand=_build(children[0]),
            span=span,
        )

    # Parentheses group expressions but do not need
    # separate AST node types. The outer span is kept.

    if kind in ("grouped_expression", "grouped_condition"):
        return replace(
            _build(children[0]),
            span=span,
        )

    # Binary arithmetic operations

    if kind in ("sum_expr", "product_expr"):
        result = _build(children[0])

        for index in range(1, len(children), 2):
            right = _build(children[index + 1])
            operator = str(children[index])

            result = BinaryExpression(
                operator=operator,
                left=result,
                right=right,
                span=SourceSpan(
                    start_line=result.span.start_line,
                    start_column=result.span.start_column,
                    end_line=right.span.end_line,
                    end_column=right.span.end_column,
                    start_pos=result.span.start_pos,
                    end_pos=right.span.end_pos,
                ),
            )

        return result

    # Boolean conditions

    if kind == "comparison":
        return Comparison(
            left=_build(children[0]),
            operator=str(children[1]),
            right=_build(children[2]),
            span=span,
        )

    if kind == "not_condition":
        return LogicalNot(
            operand=_build(children[0]),
            span=span,
        )

    if kind == "or_condition":
        result = _build(children[0])

        for next_condition in children[1:]:
            right = _build(next_condition)

            result = LogicalOr(
                left=result,
                right=right,
                span=SourceSpan(
                    start_line=result.span.start_line,
                    start_column=result.span.start_column,
                    end_line=right.span.end_line,
                    end_column=right.span.end_column,
                    start_pos=result.span.start_pos,
                    end_pos=right.span.end_pos,
                ),
            )

        return result

    raise ValueError(
        f"Unsupported SIPL parse rule: {kind}"
    )


def parse_ast(source: str) -> Program:
    """Parse SIPL source into typed AST nodes with source positions."""

    result = _build(parse_source(source))

    if not isinstance(result, Program):
        raise TypeError("Expected a SIPL Program node")

    return result


def parse_ast_file(path: str) -> Program:
    """Read a UTF-8 SIPL file and return its typed AST."""

    with open(path, encoding="utf-8-sig") as stream:
        return parse_ast(stream.read())
