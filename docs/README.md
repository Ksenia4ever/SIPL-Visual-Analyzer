# SIPL Visual Analyzer — Technical Documentation

## 1. Architecture

SIPL Visual Analyzer has a modular architecture.

```text
                   SIPL Source
                        |
                        v
                   Lark Grammar
                        |
              +---------+---------+
              |                   |
              v                   v
             CST                 AST
              |                   |
              v                   +---- Interpreter
    VIS-01 Visualization          |
              |                   v
              |             VIS-02 Visualization
              |                   |
              +---------+---------+
                        |
                        v
                 CST/AST Comparison
```

The project uses the same formal grammar
for all parsing and visualization operations.

## 2. CORE-01: Formal Grammar

Source grammar:

`src/sipl/grammar.lark`

The grammar supports:

- Assignment
- Sequential composition
- Conditional statements
- While loops
- Blocks
- Skip
- Arithmetic and Boolean expressions

## 3. CORE-02: Typed AST

AST data model:

`src/sipl/ast.py`

AST parser:

`src/sipl/parser.py`

AST nodes are custom immutable dataclasses.

Every node includes a SourceSpan.

## 4. CORE-03: Interpreter

Implementation:

`src/sipl/interpreter/runtime.py`

The interpreter executes typed AST nodes.

It supports variable state, arithmetic,
conditions, loops and execution limits.

## 5. CORE-05: Command Line Interface

Implementation:

`src/sipl/cli.py`

Commands:

- check
- parse
- run
- trace

The CLI provides text and JSON output
and documented exit codes.

## 6. VIS-01: Concrete Syntax Tree

Implementation:

`src/sipl/visualization/tree.py`

CLI entry point:

`src/sipl/visualization/__main__.py`

CST is generated using Lark
with keep_all_tokens=True.

CST preserves:

- Grammar rules
- Keywords
- Punctuation
- Operators
- Literal terminals
- Source positions

VIS-01 supports:

- Text
- JSON
- DOT
- SVG

## 7. VIS-02: Abstract Syntax Tree

Implementation:

`src/sipl/visualization/ast_tree.py`

CLI entry point:

`src/sipl/visualization/ast_cli.py`

VIS-02 traverses the custom AST from CORE-02.

It does not use a new grammar or duplicate
the original AST parser.

Each exported AST node contains:

- id
- kind
- name
- role
- span
- attributes
- children

Node IDs are assigned using preorder traversal.

Each child has a role describing the original
AST field from which it was obtained.

Examples:

- body
- condition
- then_branch
- else_branch
- statements[0]
- left
- right

## 8. AST Source Positions

SourceSpan contains:

- start_line
- start_column
- end_line
- end_column
- start_pos
- end_pos

Line and column positions are 1-based.

Character positions are 0-based,
and end positions are exclusive.

These positions are taken from CORE-02 AST nodes.

## 9. AST Visualization Formats

### Text

An indented representation of typed AST nodes.

### JSON

A structured representation suitable for
automated analysis and integrations.

### DOT

A Graphviz directed graph.

Nodes display:

- Class name
- Source position
- Scalar attributes

Edges display the field role.

### SVG

A browser-compatible diagram generated
from the DOT representation.

## 10. CST/AST Comparison

VIS-02 provides two comparison formats:

- JSON
- HTML

Comparison JSON contains:

- schema_version
- summary
- ast
- cst

The summary contains:

- ast_nodes
- cst_nodes
- cst_rule_nodes
- cst_token_nodes
- ast_node_types

The HTML comparison displays CST and AST
side by side with embedded SVG diagrams.

It also includes:

- Node counts
- Terminal count
- Original SIPL program

The HTML file is self-contained and
can be opened locally in a web browser.

## 11. Meaning of the Comparison

CST describes how the source code follows
the formal grammar.

AST describes the program structure
without unnecessary syntactic symbols.

For example, CST contains terminal nodes
for begin, end, semicolons and assignment.

AST represents these constructs through
typed nodes such as Sequence and Assignment.

Both visualizations are generated from
the same input program.

## 12. AST CLI

Show help:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli --help
```

Export all formats:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format all --output output/ast_example01
```

Compare CST and AST:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format compare --output output/example01.comparison.html
```

## 13. Exit Codes

VIS-02 CLI returns:

- 0: Success
- 1: SIPL syntax error
- 2: Invalid command arguments
- 4: File system error
- 5: Graphviz or visualization error

## 14. Tests

VIS-02 tests:

`tests/test_ast_visualization.py`

The tests verify:

- AST node types
- Parent-child structure
- Operator attributes
- Source positions
- Deterministic node IDs
- Text export
- JSON export
- DOT export
- SVG generation
- CST/AST comparison statistics
- HTML generation
- HTML escaping
- Command-line execution
- Invalid SIPL programs
- Missing files
- Complete export generation

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_ast_visualization.py -v
```

## 15. Planned Modules

SEM-01 will generate formal semantic terms
from typed AST nodes.

REL-02 will produce a tagged public release
with supporting documentation and artifacts.
