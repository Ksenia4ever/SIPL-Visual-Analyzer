"""Tests for VIS-01: SIPL concrete parse-tree visualization."""

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from sipl.syntax import SIPLSyntaxError

from sipl.visualization import (
    get_visualization_parser,
    parse_cst,
    tree_to_data,
    tree_to_dot,
    tree_to_json,
    tree_to_text,
    write_svg,
)


SOURCE = (
    "begin "
    "X := 2; "
    "if X > 0 then skip else X := 0 "
    "end"
)


def walk(node):
    """Visit all serialized tree nodes recursively."""

    yield node

    for child in node["children"]:
        yield from walk(child)


def invoke(*args):
    """Run visualization as an actual Python subprocess."""

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "sipl.visualization",
            *map(str, args),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_parse_tree_root():
    tree = parse_cst(SOURCE)
    data = tree_to_data(tree)

    assert data["kind"] == "rule"
    assert data["name"] == "start"
    assert data["id"] == "n1"


def test_cst_preserves_literal_tokens():
    data = tree_to_data(parse_cst(SOURCE))

    values = [
        node["value"]
        for node in walk(data)
        if node["kind"] == "token"
    ]

    assert "begin" in values
    assert "end" in values
    assert ":=" in values
    assert ";" in values
    assert "if" in values
    assert "then" in values
    assert "else" in values


def test_tree_contains_real_rules():
    data = tree_to_data(parse_cst(SOURCE))

    names = {
        node["name"]
        for node in walk(data)
        if node["kind"] == "rule"
    }

    assert "start" in names
    assert "sequence" in names
    assert "assignment" in names
    assert "conditional" in names
    assert "comparison" in names


def test_root_source_span():
    data = tree_to_data(parse_cst(SOURCE))
    span = data["span"]

    assert span["start_pos"] == 0
    assert span["end_pos"] == len(SOURCE)

    assert (
        SOURCE[span["start_pos"]:span["end_pos"]]
        == SOURCE
    )


def test_every_token_source_span():
    data = tree_to_data(parse_cst(SOURCE))

    for node in walk(data):
        if node["kind"] != "token":
            continue

        span = node["span"]

        original = SOURCE[
            span["start_pos"]:span["end_pos"]
        ]

        assert original == node["value"]
        assert span["start_line"] >= 1
        assert span["start_column"] >= 1


def test_unique_preorder_node_ids():
    data = tree_to_data(parse_cst(SOURCE))
    nodes = list(walk(data))

    ids = [node["id"] for node in nodes]

    assert len(ids) == len(set(ids))

    assert ids == [
        f"n{index}"
        for index in range(1, len(ids) + 1)
    ]


def test_json_export():
    result = tree_to_json(parse_cst(SOURCE))

    data = json.loads(result)

    assert data["name"] == "start"
    assert data["children"]
    assert data["span"]["start_line"] == 1


def test_json_supports_unicode():
    source = (
        "begin "
        "if ¬ (X = 0 ∨ Y > 2) "
        "then skip else X := 3 "
        "end"
    )

    exported = tree_to_json(parse_cst(source))

    assert "¬" in exported
    assert "∨" in exported


def test_text_export():
    result = tree_to_text(parse_cst(SOURCE))

    assert "start" in result
    assert "assignment" in result
    assert "conditional" in result
    assert "1:1" in result
    assert "begin" in result


def test_dot_export():
    result = tree_to_dot(parse_cst(SOURCE))

    assert "digraph SIPL_CST" in result
    assert "->" in result
    assert "shape=box" in result
    assert "shape=ellipse" in result


def test_deterministic_export():
    first = tree_to_json(parse_cst(SOURCE))
    second = tree_to_json(parse_cst(SOURCE))

    assert first == second


def test_parser_cache():
    assert (
        get_visualization_parser()
        is get_visualization_parser()
    )


def test_invalid_sipl():
    with pytest.raises(SIPLSyntaxError):
        parse_cst("begin X = 5 end")


def test_cli_text_output(tmp_path):
    source_file = tmp_path / "sample.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(source_file, "--format", "text")

    assert result.returncode == 0
    assert "assignment" in result.stdout


def test_cli_json_file(tmp_path):
    source_file = tmp_path / "sample.sipl"
    output_file = tmp_path / "tree.json"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "json",
        "--output",
        output_file,
    )

    assert result.returncode == 0
    assert output_file.exists()

    data = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert data["name"] == "start"


def test_cli_dot_file(tmp_path):
    source_file = tmp_path / "sample.sipl"
    output_file = tmp_path / "tree.dot"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "dot",
        "--output",
        output_file,
    )

    assert result.returncode == 0
    assert output_file.exists()
    assert "digraph" in output_file.read_text(
        encoding="utf-8"
    )


def test_cli_missing_source_file(tmp_path):
    result = invoke(
        tmp_path / "missing.sipl",
        "--format",
        "text",
    )

    assert result.returncode == 4
    assert "File error" in result.stderr


def test_cli_syntax_error(tmp_path):
    source_file = tmp_path / "invalid.sipl"

    source_file.write_text(
        "begin X = 5 end",
        encoding="utf-8",
    )

    result = invoke(source_file, "--format", "text")

    assert result.returncode == 1
    assert "Syntax error" in result.stderr


def test_cli_svg_requires_output(tmp_path):
    source_file = tmp_path / "sample.sipl"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(source_file, "--format", "svg")

    assert result.returncode == 2
    assert "--output" in result.stderr


@pytest.mark.skipif(
    shutil.which("dot") is None,
    reason="Graphviz executable is not installed",
)
def test_svg_generation(tmp_path):
    destination = tmp_path / "tree.svg"

    result = write_svg(
        parse_cst(SOURCE),
        destination,
    )

    assert result == destination
    assert destination.exists()

    assert "<svg" in destination.read_text(
        encoding="utf-8"
    )


@pytest.mark.skipif(
    shutil.which("dot") is None,
    reason="Graphviz executable is not installed",
)
def test_cli_all_formats(tmp_path):
    source_file = tmp_path / "sample.sipl"
    output_directory = tmp_path / "visualizations"

    source_file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    result = invoke(
        source_file,
        "--format",
        "all",
        "--output",
        output_directory,
    )

    assert result.returncode == 0

    for extension in ("txt", "json", "dot", "svg"):
        assert (
            output_directory
            / f"sample.cst.{extension}"
        ).exists()
