"""VIS-02 AST export and CST/AST comparison tests."""

import json
from pathlib import Path
import subprocess
import sys

from sipl.parser import parse_ast
from sipl.visualization.tree import parse_cst

from sipl.visualization.ast_tree import (
    ast_to_data,
    ast_to_dot,
    ast_to_json,
    ast_to_text,
    comparison_data,
    comparison_json,
    render_dot_svg,
    write_ast_svg,
    write_comparison_html,
)


SOURCE = (
    "begin X := 2 + 3 * 4; "
    "while X > 0 do X := X - 1 end"
)


def nodes(node):
    yield node

    for child in node["children"]:
        yield from nodes(child)


def invoke(*args):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "sipl.visualization.ast_cli",
            *map(str, args),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_ast_root_and_typed_nodes():
    data = ast_to_data(parse_ast(SOURCE))

    assert data["id"] == "a1"
    assert data["name"] == "Program"
    assert data["kind"] == "ast"

    assert {
        n["name"] for n in nodes(data)
    } >= {
        "Program",
        "Sequence",
        "Assignment",
        "BinaryExpression",
        "WhileStatement",
    }


def test_ast_operator_attributes_and_roles():
    data = ast_to_data(parse_ast(SOURCE))

    binary = [
        n for n in nodes(data)
        if n["name"] == "BinaryExpression"
    ]

    assert {
        n["attributes"]["operator"]
        for n in binary
    } >= {"+", "*", "-"}

    assert "statements[0]" in [
        n["role"] for n in nodes(data)
    ]


def test_ast_no_punctuation_tokens():
    data = ast_to_data(parse_ast(SOURCE))

    assert not any(
        n["kind"] == "token"
        for n in nodes(data)
    )

    assert not any(
        n["name"] == "SEMICOLON"
        for n in nodes(data)
    )


def test_ast_unique_stable_ids():
    first = ast_to_data(parse_ast(SOURCE))
    second = ast_to_data(parse_ast(SOURCE))

    ids = [
        n["id"] for n in nodes(first)
    ]

    assert ids == [
        f"a{i}" for i in range(1, len(ids) + 1)
    ]

    assert first == second


def test_all_ast_spans_point_into_source():
    data = ast_to_data(parse_ast(SOURCE))

    for item in nodes(data):
        span = item["span"]

        assert (
            0 <= span["start_pos"]
            < span["end_pos"]
            <= len(SOURCE)
        )

        assert span["start_line"] >= 1

        assert SOURCE[
            span["start_pos"]:span["end_pos"]
        ]


def test_ast_json_unicode():
    source = (
        "begin "
        "if ¬ (X = 0 ∨ Y > 2) "
        "then skip else X := 3 "
        "end"
    )

    data = json.loads(
        ast_to_json(parse_ast(source))
    )

    assert data["name"] == "Program"

    assert any(
        n["name"] == "LogicalNot"
        for n in nodes(data)
    )


def test_ast_text_format():
    output = ast_to_text(
        parse_ast(SOURCE)
    )

    assert "Program" in output
    assert "BinaryExpression" in output
    assert "operator='*'" in output
    assert "1:1-" in output


def test_ast_dot_format():
    output = ast_to_dot(
        parse_ast(SOURCE)
    )

    assert "digraph SIPL_AST" in output
    assert "->" in output
    assert "BinaryExpression" in output
    assert "statements[0]" in output


def test_comparison_counts():
    result = comparison_data(
        parse_ast(SOURCE),
        parse_cst(SOURCE),
    )

    summary = result["summary"]

    assert (
        summary["cst_nodes"]
        > summary["ast_nodes"]
    )

    assert summary["cst_token_nodes"] > 0
    assert summary["cst_rule_nodes"] > 0

    assert (
        summary["ast_node_types"]["Program"]
        == 1
    )


def test_comparison_json():
    output = json.loads(
        comparison_json(
            parse_ast(SOURCE),
            parse_cst(SOURCE),
        )
    )

    assert output["schema_version"] == "1.0"
    assert output["ast"]["name"] == "Program"
    assert output["cst"]["name"] == "start"


def test_svg_string():
    svg = render_dot_svg(
        ast_to_dot(parse_ast(SOURCE))
    )

    assert "<svg" in svg
    assert "BinaryExpression" in svg


def test_svg_file(tmp_path):
    path = tmp_path / "a" / "tree.svg"

    assert write_ast_svg(
        parse_ast(SOURCE),
        path,
    ) == path

    assert "<svg" in path.read_text(
        encoding="utf-8"
    )


def test_comparison_html_file(tmp_path):
    path = tmp_path / "comparison.html"

    write_comparison_html(
        parse_ast(SOURCE),
        parse_cst(SOURCE),
        SOURCE,
        path,
        "program.sipl",
    )

    output = path.read_text(
        encoding="utf-8"
    )

    assert "CST — concrete syntax" in output
    assert "AST — abstract syntax" in output
    assert output.count("<svg") == 2
    assert "program.sipl" in output


def test_html_escapes_filename(tmp_path):
    path = tmp_path / "comparison.html"

    write_comparison_html(
        parse_ast(SOURCE),
        parse_cst(SOURCE),
        SOURCE,
        path,
        "<script>",
    )

    text = path.read_text(
        encoding="utf-8"
    )

    assert "&lt;script&gt;" in text
    assert "<script>" not in text


def test_cli_text(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "text",
    )

    assert result.returncode == 0
    assert "Program" in result.stdout


def test_cli_json(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "json",
    )

    assert result.returncode == 0

    assert (
        json.loads(result.stdout)["name"]
        == "Program"
    )


def test_cli_dot_file(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    destination = tmp_path / "sub" / "ast.dot"

    result = invoke(
        source_file,
        "--format",
        "dot",
        "--output",
        destination,
    )

    assert result.returncode == 0

    assert "digraph SIPL_AST" in (
        destination.read_text(encoding="utf-8")
    )


def test_cli_compare_json(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "compare-json",
    )

    assert result.returncode == 0

    assert (
        json.loads(result.stdout)
        ["summary"]["cst_nodes"]
        > 0
    )


def test_cli_compare_html(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    destination = tmp_path / "compare.html"

    result = invoke(
        source_file,
        "--format",
        "compare",
        "--output",
        destination,
    )

    assert result.returncode == 0
    assert destination.exists()

    assert "<svg" in destination.read_text(
        encoding="utf-8"
    )


def test_cli_all(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    target = tmp_path / "all"

    result = invoke(
        source_file,
        "--format",
        "all",
        "--output",
        target,
    )

    assert result.returncode == 0, result.stderr

    for name in (
        "program.ast.txt",
        "program.ast.json",
        "program.ast.dot",
        "program.ast.svg",
        "program.comparison.json",
        "program.comparison.html",
    ):
        assert (target / name).exists(), name


def test_cli_missing_output_for_svg(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "svg",
    )

    assert result.returncode == 2
    assert "--output" in result.stderr


def test_cli_invalid_program(tmp_path):
    source_file = tmp_path / "bad.sipl"

    source_file.write_text(
        "begin X = 1 end",
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "json",
    )

    assert result.returncode == 1
    assert "Syntax error" in result.stderr


def test_cli_missing_file(tmp_path):
    result = invoke(
        tmp_path / "missing.sipl",
        "--format",
        "json",
    )

    assert result.returncode == 4
    assert "File error" in result.stderr


def test_cli_svg_file(tmp_path):
    source_file = tmp_path / "program.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    destination = tmp_path / "ast.svg"

    result = invoke(
        source_file,
        "--format",
        "svg",
        "--output",
        destination,
    )

    assert result.returncode == 0
    assert destination.exists()
