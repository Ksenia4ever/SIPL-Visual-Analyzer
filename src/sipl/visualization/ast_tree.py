"""VIS-02: typed SIPL AST visualization and CST comparison."""

from collections import Counter
from dataclasses import fields
from html import escape
import json
from pathlib import Path
import subprocess

from sipl.ast import Node, Program
from sipl.visualization.tree import tree_to_data, tree_to_dot


def _span_data(node: Node) -> dict[str, int]:
    """Convert SourceSpan to a JSON-compatible dictionary."""

    return {
        item.name: getattr(node.span, item.name)
        for item in fields(node.span)
    }


def ast_to_data(program: Program) -> dict:
    """Serialize custom AST nodes with stable preorder IDs."""

    counter = 0

    def convert(
        node: Node,
        role: str = "root",
    ) -> dict:
        nonlocal counter

        counter += 1

        result = {
            "id": f"a{counter}",
            "kind": "ast",
            "name": type(node).__name__,
            "role": role,
            "span": _span_data(node),
            "attributes": {},
            "children": [],
        }

        for field in fields(node):
            if field.name == "span":
                continue

            value = getattr(node, field.name)

            if isinstance(value, Node):
                result["children"].append(
                    convert(value, field.name)
                )

            elif isinstance(value, (tuple, list)):
                for index, child in enumerate(value):
                    if not isinstance(child, Node):
                        raise TypeError(
                            f"Unsupported AST child in {field.name}"
                        )

                    result["children"].append(
                        convert(
                            child,
                            f"{field.name}[{index}]",
                        )
                    )

            elif isinstance(value, (str, int, bool)):
                result["attributes"][field.name] = value

            else:
                raise TypeError(
                    f"Unsupported AST attribute: {field.name}"
                )

        return result

    return convert(program)


def ast_to_json(program: Program) -> str:
    """Export the AST as formatted JSON."""

    return json.dumps(
        ast_to_data(program),
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def ast_to_text(program: Program) -> str:
    """Export the AST as a readable, indented tree."""

    rows = []

    def visit(node: dict, depth: int) -> None:
        span = node["span"]

        attributes = " ".join(
            f"{name}={value!r}"
            for name, value in node["attributes"].items()
        )

        rows.append(
            f"{'  ' * depth}{node['id']} "
            f"{node['role']}: {node['name']} "
            f"[{span['start_line']}:{span['start_column']}-"
            f"{span['end_line']}:{span['end_column']}]"
            + (f" {attributes}" if attributes else "")
        )

        for child in node["children"]:
            visit(child, depth + 1)

    visit(ast_to_data(program), 0)

    return "\n".join(rows) + "\n"


def _dot_quote(value: str) -> str:
    """Escape text for Graphviz DOT labels."""

    return (
        '"'
        + value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        + '"'
    )


def ast_to_dot(program: Program) -> str:
    """Generate a Graphviz DOT graph from the typed AST."""

    root = ast_to_data(program)

    rows = [
        "digraph SIPL_AST {",
        "  rankdir=TB;",
        (
            '  graph [bgcolor="white", '
            'pad=0.3, nodesep=0.35];'
        ),
        (
            '  node [shape=box, '
            'style="rounded,filled", '
            'fillcolor="#EAF2FF", '
            'color="#5685C4", '
            'fontname="Arial", fontsize=11];'
        ),
        (
            '  edge [color="#64748B", '
            'fontname="Arial", fontsize=9];'
        ),
    ]

    def visit(node: dict) -> None:
        span = node["span"]

        label = (
            f"{node['name']}\n"
            f"{span['start_line']}:"
            f"{span['start_column']}–"
            f"{span['end_line']}:"
            f"{span['end_column']}"
        )

        for name, value in node["attributes"].items():
            label += f"\n{name} = {value}"

        rows.append(
            f"  {node['id']} "
            f"[label={_dot_quote(label)}];"
        )

        for child in node["children"]:
            rows.append(
                f"  {node['id']} -> {child['id']} "
                f"[label={_dot_quote(child['role'])}];"
            )

            visit(child)

    visit(root)

    rows.append("}")

    return "\n".join(rows) + "\n"


def render_dot_svg(dot_source: str) -> str:
    """Render DOT to an SVG string using system Graphviz."""

    try:
        result = subprocess.run(
            ["dot", "-Tsvg"],
            input=dot_source,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "Graphviz 'dot' was not found. "
            "Install Graphviz and add it to PATH."
        ) from error

    if result.returncode != 0:
        raise RuntimeError(
            "Graphviz SVG generation failed: "
            + result.stderr.strip()
        )

    # Remove XML declaration and DOCTYPE from
    # Graphviz output before embedding into HTML.
    svg_start = result.stdout.find("<svg")

    if svg_start < 0:
        raise RuntimeError(
            "Graphviz returned no SVG element"
        )

    return result.stdout[svg_start:]


def write_ast_svg(
    program: Program,
    path: str | Path,
) -> Path:
    """Create an SVG representation of the typed AST."""

    destination = Path(path)

    svg = render_dot_svg(
        ast_to_dot(program)
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        svg,
        encoding="utf-8",
    )

    return destination


def comparison_data(
    program: Program,
    cst,
) -> dict:
    """Build a combined AST/CST model and summary."""

    ast = ast_to_data(program)
    concrete = tree_to_data(cst)

    def walk(node: dict):
        yield node

        for child in node["children"]:
            yield from walk(child)

    ast_nodes = list(walk(ast))
    concrete_nodes = list(walk(concrete))

    token_count = sum(
        node["kind"] == "token"
        for node in concrete_nodes
    )

    node_types = Counter(
        node["name"]
        for node in ast_nodes
    )

    return {
        "schema_version": "1.0",
        "summary": {
            "ast_nodes": len(ast_nodes),
            "cst_nodes": len(concrete_nodes),
            "cst_rule_nodes": (
                len(concrete_nodes) - token_count
            ),
            "cst_token_nodes": token_count,
            "ast_node_types": dict(
                sorted(node_types.items())
            ),
        },
        "ast": ast,
        "cst": concrete,
    }


def comparison_json(
    program: Program,
    cst,
) -> str:
    """Export comparison information as JSON."""

    return json.dumps(
        comparison_data(program, cst),
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def write_comparison_html(
    program: Program,
    cst,
    source: str,
    path: str | Path,
    source_name: str = "SIPL program",
) -> Path:
    """Generate a side-by-side CST/AST HTML report."""

    summary = comparison_data(
        program,
        cst,
    )["summary"]

    cst_svg = render_dot_svg(
        tree_to_dot(cst)
    )

    ast_svg = render_dot_svg(
        ast_to_dot(program)
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SIPL CST vs AST — {escape(source_name, quote=True)}</title>
<style>
:root {{
    font-family: Segoe UI, Arial, sans-serif;
    color: #182536;
    background: #f5f7fb;
}}
body {{ margin: 0; padding: 24px; }}
h1 {{ margin: 0 0 8px; }}
p {{ line-height: 1.5; }}
.metrics {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 16px 0 24px;
}}
.metric {{
    background: white;
    border: 1px solid #e0e5ed;
    padding: 12px 18px;
    border-radius: 10px;
}}
.metric strong {{
    font-size: 22px;
    display: block;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(2,minmax(0,1fr));
    gap: 18px;
}}
.panel {{
    background: white;
    border: 1px solid #e0e5ed;
    border-radius: 12px;
    padding: 14px;
    min-width: 0;
}}
.canvas {{
    overflow: auto;
    max-height: 75vh;
    border-top: 1px solid #e0e5ed;
    padding-top: 14px;
}}
.canvas svg {{
    max-width: none;
    height: auto;
}}
pre {{
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    background: #e9eff8;
    padding: 14px;
    border-radius: 10px;
}}
small {{ color: #556579; }}
@media (max-width: 1000px) {{
    .grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<h1>SIPL: Concrete Syntax Tree vs Abstract Syntax Tree</h1>
<p><strong>Source:</strong> {escape(source_name)}.
Both trees come from the same input and grammar.</p>
<div class="metrics">
<div class="metric"><strong>{summary['cst_nodes']}</strong>CST nodes</div>
<div class="metric"><strong>{summary['cst_token_nodes']}</strong>CST terminal tokens</div>
<div class="metric"><strong>{summary['ast_nodes']}</strong>AST nodes</div>
</div>
<div class="grid">
<section class="panel">
<h2>CST — concrete syntax</h2>
<p>Contains grammar rules, keywords and punctuation.</p>
<div class="canvas">{cst_svg}</div>
</section>
<section class="panel">
<h2>AST — abstract syntax</h2>
<p>Contains typed program structures and source positions;
punctuation is omitted.</p>
<div class="canvas">{ast_svg}</div>
</section>
</div>
<h2>Original SIPL source</h2>
<pre>{escape(source)}</pre>
<small>Lines and columns are 1-based.
End positions are exclusive.</small>
</body>
</html>
"""

    destination = Path(path)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        html,
        encoding="utf-8",
    )

    return destination
