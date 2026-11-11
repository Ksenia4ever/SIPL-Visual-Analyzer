# SIPL Visual Analyzer v1.0.0

First completed educational release of SIPL Visual Analyzer.

## Overview

SIPL Visual Analyzer is a Python toolkit developed for the
Theory of Programming course.

It provides syntax analysis, program execution, visualization
and formal semantic-term generation for SIPL.

## Included Modules

### CORE-01 — Formal SIPL Grammar
- Machine-readable grammar implemented with Lark
- Syntax checking and diagnostics
- Positive and negative syntax tests

### CORE-02 — Typed AST
- Custom immutable AST nodes
- Recursive parsing from Lark
- SourceSpan support

### CORE-03 — SIPL Interpreter
- Assignment, sequence, conditionals and loops
- Arithmetic and Boolean expressions
- Variable state management
- Runtime errors and step limits

### CORE-05 — Command-Line Interface
- check
- parse
- run
- trace
- JSON output and documented exit codes

### VIS-01 — Concrete Syntax Tree Visualization
- TXT
- JSON
- DOT
- SVG

### VIS-02 — AST Visualization and Comparison
- Typed AST visualization
- CST/AST comparison JSON
- Side-by-side HTML comparison

### SEM-01 — Semantic Term Generation
- Recursive AST-to-term transformation
- ASIPL notation from the course
- Text and JSON output
- Golden tests

## Installation

Python 3.11 or newer is required.

Download the wheel file from the release assets.

Install the package:

```powershell
py -m pip install .\sipl_visual_analyzer-1.0.0-py3-none-any.whl
```

The command-line interface is available as `sipl`.

Graphviz is required for SVG and HTML visualization.

## Basic Commands

Check syntax:

```powershell
sipl check examples/valid_loop.sipl
```

Parse the program:

```powershell
sipl parse examples/example01.sipl
```

Run the interpreter:

```powershell
sipl run examples/example01.sipl --state X=2 --state Y=3
```

Trace execution:

```powershell
sipl trace examples/valid_loop.sipl
```

Generate semantic terms:

```powershell
python -m sipl.semantics examples/example01.sipl
```

Generate CST:

```powershell
python -m sipl.visualization examples/example01.sipl --format all --output output/cst
```

Generate AST and comparison:

```powershell
python -m sipl.visualization.ast_cli examples/example01.sipl --format all --output output/ast
```

These example commands assume execution from a project checkout
containing the examples directory.

## Release Assets

- Wheel distribution (.whl)
- Source distribution (.tar.gz)

GitHub also provides source archives automatically.

## Verification

The release was prepared with automated pytest tests
and distribution validation.

See the repository README for complete setup,
testing and usage instructions.

## Notes

This release implements the basic SIPL language
described in the coursework.

The `SEM-01` module constructs formal semantic terms.
It does not evaluate those terms on states.

The external Graphviz application is required for
SVG rendering.

## License

MIT License.
