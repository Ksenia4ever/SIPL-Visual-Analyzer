# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit for
SIPL (Simple Programming Language), developed for the
Theory of Programming course.

It supports formal grammar analysis, typed AST construction,
program execution, visualization and semantic-term generation.

## Selected Coursework Tasks

| Task ID | Module | Points |
|---------|--------|--------|
| CORE-01 | Formal SIPL Grammar | 0.5 |
| CORE-02 | Parser and Typed AST | 1.5 |
| CORE-03 | SIPL Interpreter | 2.0 |
| CORE-05 | Command-Line Interface | 1.0 |
| VIS-01 | Parse Tree Visualization | 1.5 |
| VIS-02 | AST Visualization and Comparison | 1.0 |
| SEM-01 | Semantic Term Generation | 2.0 |
| REL-02 | GitHub Release | 0.5 |
| **Total** | | **10.0** |

The table describes the selected coursework scope,
not the instructor's final assessment.

## Release

**Version:** 1.0.0

**License:** MIT

**Python:** 3.11+

See `CHANGELOG.md` and `docs/RELEASE_NOTES_v1.0.0.md`
for release information.

## Features

### Formal Grammar — CORE-01
- Lark-based SIPL grammar
- Lexical specification
- Positive and negative syntax tests
- Syntax error diagnostics

### Parser — CORE-02
- Custom typed AST
- SourceSpan coordinates
- AST construction from Lark

### Interpreter — CORE-03
- Assignments and sequential execution
- If/then/else and while loops
- Begin/end and skip
- Arithmetic and Boolean conditions
- Variable state
- Step limits and runtime diagnostics

### CLI — CORE-05
- check
- parse
- run
- trace
- JSON responses
- Documented exit codes

### CST Visualization — VIS-01
- Text, JSON, DOT and SVG
- Source-linked grammar nodes

### AST Visualization — VIS-02
- Text, JSON, DOT and SVG
- Side-by-side HTML CST/AST comparison
- Source positions and node statistics

### Formal Semantics — SEM-01
- Recursive semantic-term construction
- ASIPL course notation
- Text and JSON output
- Golden tests

## Technologies

- Python 3.11+
- Lark
- pytest
- pytest-cov
- Graphviz
- Git and GitHub

## Project Structure

```text
SIPL-Visual-Analyzer/
├── grammar/
│   └── README.md
├── src/
│   └── sipl/
│       ├── __init__.py
│       ├── ast.py
│       ├── cli.py
│       ├── grammar.lark
│       ├── parser.py
│       ├── syntax.py
│       ├── interpreter/
│       │   ├── __init__.py
│       │   ├── runtime.py
│       │   └── tracing.py
│       ├── semantics/
│       │   ├── __init__.py
│       │   ├── __main__.py
│       │   └── terms.py
│       └── visualization/
│           ├── __init__.py
│           ├── __main__.py
│           ├── tree.py
│           ├── ast_tree.py
│           └── ast_cli.py
├── examples/
├── grammar/
├── docs/
│   ├── README.md
│   └── RELEASE_NOTES_v1.0.0.md
├── tests/
│   ├── golden/
│   │   └── semantic_terms.json
│   └── test_*.py
├── pyproject.toml
├── MANIFEST.in
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Installation from Source

Download the repository ZIP archive from GitHub
and extract it.

Open the project folder in VS Code.

Create a virtual environment:

```powershell
py -m venv .venv
```

Install the project with development dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

The CLI is available through:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli --help
```

Or:

```powershell
.\.venv\Scripts\sipl.exe --help
```

## Install from Release Wheel

Download the `.whl` file from the GitHub Release.

Install:

```powershell
py -m pip install .\sipl_visual_analyzer-1.0.0-py3-none-any.whl
```

A wheel installation contains the Python package,
but not the repository examples and test suite.

Download the repository source archive if you
want to run the examples or the tests.

## Graphviz Installation

Graphviz is required for SVG visualization.

Windows:

```powershell
winget install --id Graphviz.Graphviz -e
```

Check:

```powershell
dot -V
```

## Main CLI

### Check SIPL Syntax

```powershell
.\.venv\Scripts\python.exe -m sipl.cli check examples/valid_loop.sipl
```

### Parse SIPL to AST

```powershell
.\.venv\Scripts\python.exe -m sipl.cli parse examples/example01.sipl
```

### Run a SIPL Program

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/interpreter_demo.sipl
```

Expected result:

```text
Execution completed successfully.

Final state:
  Result = 30
  X = 0

Steps: 18
```

### Initial Variable Values

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/example01.sipl --state X=2 --state Y=3
```

The example calculates 2 to the power of 3
using repeated multiplication.

Expected final values:

```text
R = 8
X = 2
Y = 0
```

### Trace

```powershell
.\.venv\Scripts\python.exe -m sipl.cli trace examples/valid_loop.sipl
```

### JSON Output

Use `--json` with check, parse, run or trace:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/interpreter_demo.sipl --json
```

Main CLI exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | SIPL syntax error |
| 2 | Invalid CLI arguments |
| 3 | SIPL runtime error |
| 4 | File reading error |

## VIS-01: CST Visualization

Generate all concrete syntax-tree exports:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization examples/example01.sipl --format all --output output/example01
```

The command generates:

- TXT
- JSON
- DOT
- SVG

The CST contains grammar rules, terminal tokens
and source positions.

## VIS-02: AST Visualization

Generate typed AST and comparison outputs:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format all --output output/ast_example01
```

Generated files include:

- AST TXT
- AST JSON
- AST DOT
- AST SVG
- Comparison JSON
- Comparison HTML

The HTML report shows CST and AST side by side.

## SEM-01: Semantic Terms

Generate an ASIPL semantic term:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl
```

Generate JSON:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl --format json
```

Save a term to a file:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl --output output/example01.semantic.txt
```

The module generates formal terms recursively
from the typed AST.

It supports assignments, sequences, conditionals,
loops, blocks, skip, arithmetic and Boolean operations.

The semantics module constructs terms; it does not
evaluate those terms against a state.

## Python API

```python
from sipl.parser import parse_ast
from sipl.interpreter import run_source
from sipl.semantics import build_term, format_term

source = "begin X := 5 end"

ast = parse_ast(source)
result = run_source(source)
term = build_term(ast)

print(result.state)
print(format_term(term))
```

Expected output:

```text
{'X': 5}
AS^X(5̅)
```

## Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Run coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

Check the interpreter coverage requirement:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_interpreter.py --cov=sipl.interpreter.runtime --cov-report=term-missing --cov-fail-under=80
```

Coverage for CLI entry points can be underestimated
when the test suite launches subprocesses.

The interpreter has a separate coverage requirement.

## Build Distribution

Install build tools:

```powershell
.\.venv\Scripts\python.exe -m pip install build twine
```

Build the wheel and source distribution:

```powershell
.\.venv\Scripts\python.exe -m build
```

Output files are placed in the `dist/` directory.

## Documentation

- `grammar/README.md`
- `docs/README.md`
- `docs/RELEASE_NOTES_v1.0.0.md`
- `CHANGELOG.md`

## References

O. V. Shyshatska, A. V. Kryvolap,
A. V. Shyshatskyi.

Theory of Programming. Practical Handbook, 2024.

M. S. Nikitchenko.

Theory of Programming, 2020.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

This project is distributed under the MIT License.

See `LICENSE`.
