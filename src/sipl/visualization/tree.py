"""Concrete SIPL parse-tree exports with source positions."""

from functools import lru_cache
from importlib.resources import files
import json
from pathlib import Path
import subprocess

from lark import Lark, Token, Tree
from lark.exceptions import UnexpectedInput

from sipl.syntax import SIPLSyntaxError


@lru_cache(maxsize=1)
def get_visualization_parser() -> Lark:
    """Preserve punctuation and keywords in the parse tree."""

    grammar = (
        files("sipl")
        .joinpath("grammar.lark")
        .read_text(encoding="utf-8")
    )

    return Lark(
        grammar,
        parser="lalr",
        lexer="contextual",
        start="start",
        propagate_positions=True,
        maybe_placeholders=False,
        keep_all_tokens=True,
    )


def parse_cst(source: str) -> Tree:
    """Build a parse tree including literal terminals."""

    try:
        return get_visualization_parser().parse(source)

    except UnexpectedInput as error:
        line = getattr(error, "line", 1) or 1
        column = getattr(error, "column", 1) or 1

        lines = source.splitlines()

        source_line = (
            lines[line - 1]
            if 1 <= line <= len(lines)
            else ""
        )

        raise SIPLSyntaxError(
            "Invalid SIPL syntax",
            line,
            column,
            source_line,
        ) from error


def _position(node: Tree | Token) -> dict[str, int]:
    """Read positions from a tree node or token."""

    meta = node.meta if isinstance(node, Tree) else node

    return {
        "start_line": meta.line,
        "start_column": meta.column,
        "end_line": meta.end_line,
        "end_column": meta.end_column,
        "start_pos": meta.start_pos,
        "end_pos": meta.end_pos,
    }


def tree_to_data(tree: Tree) -> dict:
    """Create a JSON-compatible tree with stable node IDs."""

    counter = 0

    def convert(node: Tree | Token) -> dict:
        nonlocal counter

        counter += 1
        node_id = f"n{counter}"

        if isinstance(node, Tree):
            return {
                "id": node_id,
                "kind": "rule",
                "name": str(node.data),
                "span": _position(node),
                "children": [
                    convert(child)
                    for child in node.children
                ],
            }

        return {
            "id": node_id,
            "kind": "token",
            "name": node.type,
            "value": str(node),
            "span": _position(node),
            "children": [],
        }

    return convert(tree)


def tree_to_json(tree: Tree) -> str:
    """Export the parse tree as formatted UTF-8 JSON."""

    return json.dumps(
        tree_to_data(tree),
        ensure_ascii=False,
        indent=2,
    )


def tree_to_text(tree: Tree) -> str:
    """Export an indented tree with source locations."""

    rows: list[str] = []

    def visit(node: dict, depth: int) -> None:
        span = node["span"]

        location = (
            f"{span['start_line']}:{span['start_column']}-"
            f"{span['end_line']}:{span['end_column']}"
        )

        if node["kind"] == "token":
            title = (
                f"{node['name']} "
                f"{node['value']!r}"
            )
        else:
            title = node["name"]

        rows.append(
            f"{'  ' * depth}"
            f"{node['id']} {title} [{location}]"
        )

        for child in node["children"]:
            visit(child, depth + 1)

    visit(tree_to_data(tree), 0)

    return "\n".join(rows) + "\n"


def _dot_quote(text: str) -> str:
    """Escape labels correctly for Graphviz DOT."""

    return (
        '"'
        + text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        + '"'
    )


def tree_to_dot(tree: Tree) -> str:
    """Export a Graphviz graph from the real parse tree."""

    root = tree_to_data(tree)

    rows = [
        "digraph SIPL_CST {",
        "  rankdir=TB;",
        '  node [fontname="Arial", fontsize=10];',
    ]

    def visit(node: dict) -> None:
        span = node["span"]

        location = (
            f"{span['start_line']}:"
            f"{span['start_column']}"
        )

        if node["kind"] == "token":
            label = (
                f"{node['name']}: "
                f"{node['value']}\n{location}"
            )

            rows.append(
                f'  {node["id"]} '
                f'[shape=box, label={_dot_quote(label)}];'
            )

        else:
            label = f"{node['name']}\n{location}"

            rows.append(
                f'  {node["id"]} '
                f'[shape=ellipse, label={_dot_quote(label)}];'
            )

        for child in node["children"]:
            rows.append(
                f'  {node["id"]} -> {child["id"]};'
            )

            visit(child)

    visit(root)

    rows.append("}")

    return "\n".join(rows) + "\n"


def write_svg(tree: Tree, path: str | Path) -> Path:
    """Render an SVG using the Graphviz dot executable."""

    destination = Path(path)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        process = subprocess.run(
            [
                "dot",
                "-Tsvg",
                "-o",
                str(destination),
            ],
            input=tree_to_dot(tree),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "Graphviz 'dot' executable was not found. "
            "Install Graphviz and add its bin folder to PATH."
        ) from error

    if process.returncode != 0:
        raise RuntimeError(
            "Graphviz could not generate SVG: "
            + process.stderr.strip()
        )

    return destination
