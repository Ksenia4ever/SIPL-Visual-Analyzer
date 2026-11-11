"""Tests for CORE-02: typed AST and parser."""

from pathlib import Path

import pytest

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
from sipl.parser import parse_ast, parse_ast_file
from sipl.syntax import SIPLSyntaxError


def first_statement(source: str):
    program = parse_ast(source)

    assert isinstance(program, Program)
    assert isinstance(program.body, Sequence)

    return program.body.statements[0]


def test_program_ast():
    program = parse_ast("begin skip end")

    assert isinstance(program, Program)
    assert isinstance(program.body, Sequence)
    assert len(program.body.statements) == 1


def test_skip_ast():
    statement = first_statement("begin skip end")

    assert isinstance(statement, Skip)


def test_assignment_ast():
    statement = first_statement("begin X := 5 end")

    assert isinstance(statement, Assignment)
    assert statement.name == "X"
    assert isinstance(statement.value, IntegerLiteral)
    assert statement.value.value == 5


def test_variable_expression():
    program = parse_ast("begin X := Y end")
    statement = program.body.statements[0]

    assert isinstance(statement.value, Variable)
    assert statement.value.name == "Y"


def test_sequence_ast():
    program = parse_ast("begin X := 1; Y := 2 end")

    assert isinstance(program.body, Sequence)
    assert len(program.body.statements) == 2

    assert isinstance(program.body.statements[0], Assignment)
    assert isinstance(program.body.statements[1], Assignment)


def test_addition_ast():
    statement = first_statement("begin X := 2 + 3 end")

    expression = statement.value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "+"
    assert expression.left.value == 2
    assert expression.right.value == 3


def test_subtraction_ast():
    statement = first_statement("begin X := 8 - 3 end")

    expression = statement.value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "-"


def test_multiplication_ast():
    statement = first_statement("begin X := 2 * 4 end")

    expression = statement.value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "*"


def test_arithmetic_precedence():
    statement = first_statement("begin X := 2 + 3 * 4 end")

    expression = statement.value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "+"

    assert isinstance(expression.left, IntegerLiteral)

    assert isinstance(expression.right, BinaryExpression)
    assert expression.right.operator == "*"


def test_parentheses_precedence():
    statement = first_statement("begin X := (2 + 3) * 4 end")

    expression = statement.value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "*"

    assert isinstance(expression.left, BinaryExpression)
    assert expression.left.operator == "+"


def test_unary_minus():
    statement = first_statement("begin X := -(Y + 3) end")

    expression = statement.value

    assert isinstance(expression, UnaryMinus)
    assert isinstance(expression.operand, BinaryExpression)


def test_if_statement_ast():
    source = (
        "begin "
        "if X > 0 then Y := 1 else Y := 0 "
        "end"
    )

    statement = first_statement(source)

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.condition, Comparison)

    assert statement.condition.operator == ">"
    assert isinstance(statement.then_branch, Assignment)
    assert isinstance(statement.else_branch, Assignment)


def test_while_statement_ast():
    source = (
        "begin "
        "while X > 0 do X := X - 1 "
        "end"
    )

    statement = first_statement(source)

    assert isinstance(statement, WhileStatement)
    assert isinstance(statement.condition, Comparison)
    assert isinstance(statement.body, Assignment)


def test_nested_block_ast():
    source = (
        "begin "
        "while X > 0 do "
        "begin X := X - 1; skip end "
        "end"
    )

    statement = first_statement(source)

    assert isinstance(statement, WhileStatement)
    assert isinstance(statement.body, Block)
    assert isinstance(statement.body.body, Sequence)

    assert len(statement.body.body.statements) == 2


def test_logical_conditions():
    source = (
        "begin "
        "if ¬ (X = 0 ∨ Y > 2) "
        "then skip else X := 3 "
        "end"
    )

    statement = first_statement(source)

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.condition, LogicalNot)
    assert isinstance(statement.condition.operand, LogicalOr)


def test_source_span():
    source = "begin\n    X := 5\nend"

    program = parse_ast(source)
    statement = program.body.statements[0]

    assert isinstance(program.span, SourceSpan)

    assert statement.span.start_line == 2
    assert statement.span.start_column == 5

    assert statement.span.end_line == 2
    assert statement.span.end_column == 11

    assert source[
        statement.span.start_pos:statement.span.end_pos
    ] == "X := 5"


def test_syntax_error_from_ast_parser():
    source = "begin\n    X = 5\nend"

    with pytest.raises(SIPLSyntaxError) as exc_info:
        parse_ast(source)

    error = exc_info.value

    assert error.line == 2
    assert error.column > 0
    assert "Invalid SIPL syntax" in str(error)


def test_parse_ast_file(tmp_path: Path):
    path = tmp_path / "example.sipl"
    path.write_text(
        "begin X := 10 end",
        encoding="utf-8",
    )

    program = parse_ast_file(str(path))

    assert isinstance(program, Program)
    assert isinstance(program.body, Sequence)
    assert isinstance(
        program.body.statements[0],
        Assignment,
    )
