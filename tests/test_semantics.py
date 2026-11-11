"""SEM-01 golden and integration tests."""

import json
from dataclasses import replace
from pathlib import Path
import subprocess
import sys

import pytest

from sipl.ast import Node
from sipl.parser import parse_ast

from sipl.semantics import (
    build_term,
    format_term,
    term_to_data,
)
from sipl.semantics.terms import SemanticTerm


GOLDEN = (
    Path(__file__).parent
    / "golden"
    / "semantic_terms.json"
)

CASES = json.loads(
    GOLDEN.read_text(encoding="utf-8")
)


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[case["name"] for case in CASES],
)
def test_golden_semantic_terms(case):
    program = parse_ast(case["source"])

    actual = format_term(
        build_term(program)
    )

    assert actual == case["expected"]


def test_term_is_structured_and_source_linked():
    term = build_term(
        parse_ast("begin X := 1 end")
    )

    result = term_to_data(term)

    assert result["symbol"] == "AS"
    assert result["value"] == "X"
    assert result["span"]["start_line"] == 1

    assert (
        result["arguments"][0]["symbol"]
        == "num"
    )


def test_ast_is_not_modified():
    ast = parse_ast("begin X := 1 end")

    assert build_term(ast) == build_term(ast)

    assert (
        ast.body.statements[0].name
        == "X"
    )


def test_invalid_arithmetic_operator():
    ast = parse_ast("begin X := 1 + 2 end")

    statement = ast.body.statements[0]

    invalid_value = replace(
        statement.value,
        operator="/",
    )

    bad_statement = replace(
        statement,
        value=invalid_value,
    )

    bad_body = replace(
        ast.body,
        statements=(bad_statement,),
    )

    with pytest.raises(
        ValueError,
        match="arithmetic",
    ):
        build_term(
            replace(ast, body=bad_body)
        )


def test_invalid_comparison_operator():
    ast = parse_ast(
        "begin if X > 0 then skip else skip end"
    )

    statement = ast.body.statements[0]

    bad_condition = replace(
        statement.condition,
        operator="<",
    )

    bad_statement = replace(
        statement,
        condition=bad_condition,
    )

    bad_body = replace(
        ast.body,
        statements=(bad_statement,),
    )

    with pytest.raises(
        ValueError,
        match="comparison",
    ):
        build_term(
            replace(ast, body=bad_body)
        )


def test_unsupported_node():
    span = parse_ast(
        "begin skip end"
    ).span

    with pytest.raises(
        TypeError,
        match="Unsupported AST node",
    ):
        build_term(Node(span=span))


def test_unknown_term_symbol():
    invalid = SemanticTerm("wrong")

    with pytest.raises(
        ValueError,
        match="Unknown semantic operator",
    ):
        format_term(invalid)


def test_cli_text_and_json(tmp_path):
    source = tmp_path / "test.sipl"

    source.write_text(
        "begin X := 5 end",
        encoding="utf-8",
    )

    command = [
        sys.executable,
        "-m",
        "sipl.semantics",
        str(source),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "AS^X(5̅)"

    result = subprocess.run(
        [*command, "--format", "json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0

    data = json.loads(result.stdout)

    assert data["term"] == "AS^X(5̅)"
    assert data["structure"]["symbol"] == "AS"


def test_cli_output_file(tmp_path):
    source = tmp_path / "test.sipl"
    destination = tmp_path / "nested" / "term.txt"

    source.write_text(
        "begin skip end",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sipl.semantics",
            str(source),
            "--output",
            str(destination),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0

    assert (
        destination.read_text(encoding="utf-8").strip()
        == "id"
    )


def test_cli_errors(tmp_path):
    invalid = tmp_path / "invalid.sipl"

    invalid.write_text(
        "begin X = 1 end",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sipl.semantics",
            str(invalid),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 1
    assert "Syntax error" in result.stderr

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sipl.semantics",
            str(tmp_path / "missing.sipl"),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 4
    assert "File error" in result.stderr
