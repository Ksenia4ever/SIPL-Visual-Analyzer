# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit
for the SIPL (Simple Programming Language).

Developed for the Theory of Programming course.

## Project Goal

The project implements a modular toolkit for syntax
analysis, execution, visualization and formal semantics
of SIPL programs.

## Selected Tasks

| Task ID | Description | Points |
|---------|-------------|--------|
| CORE-01 | Formal SIPL Grammar | 0.5 |
| CORE-02 | Parser and Typed AST | 1.5 |
| CORE-03 | SIPL Interpreter | 2.0 |
| CORE-05 | Command-Line Interface | 1.0 |
| VIS-01 | Parse Tree Visualization | 1.5 |
| VIS-02 | AST Visualization and Comparison | 1.0 |
| SEM-01 | Semantic Term Generation | 2.0 |
| REL-02 | GitHub Release | 0.5 |
| **Total** | | **10.0** |

Points represent the selected coursework scope,
not the instructor's final assessment.

## Implementation Status

### Implemented

- CORE-01: Formal grammar and syntax validation
- CORE-02: Typed AST with SourceSpan
- CORE-03: Interpreter and runtime diagnostics
- CORE-05: CLI and JSON interface
- VIS-01: CST visualization
- VIS-02: AST visualization and CST/AST comparison
- SEM-01: Recursive semantic-term generation
- ASIPL semantic notation
- Golden tests for semantic terms

### Planned

- REL-02: Tagged GitHub Release

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
├── tests/
│   ├── golden/
│   │   └── semantic_terms.json
│   ├── test_cli.py
│   ├── test_cli_integration.py
│   ├── test_interpreter.py
│   ├── test_parser.py
│   ├── test_parse_tree_visualization.py
│   ├── test_ast_visualization.py
│   ├── test_semantics.py
│   └── test_syntax.py
├── docs/
│   └── README.md
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

## Installation

### Requirements

- Python 3.11 or newer
- Windows PowerShell
- Graphviz for SVG visualization

Download the project and open the root directory
in Visual Studio Code.

Create a virtual environment:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Install Graphviz if it is not already available:

```powershell
winget install --id Graphviz.Graphviz -e
```

Check Graphviz:

```powershell
dot -V
```

## CORE-01: Grammar

The formal SIPL grammar is located in:

`src/sipl/grammar.lark`

Lexical specification and grammar documentation:

`grammar/README.md`

## CORE-02: Typed AST

The custom AST model is implemented in:

`src/sipl/ast.py`

AST transformation:

`src/sipl/parser.py`

Every AST node contains SourceSpan coordinates.

## CORE-03: Interpreter

The interpreter supports:

- Assignment
- Sequential composition
- Conditional statements
- While loops
- Begin/end blocks
- Skip
- Arithmetic expressions
- Boolean conditions
- Variable states
- Execution step limits

Example:

```python
from sipl.interpreter import run_source

result = run_source(
    "begin X := 2; Y := X * 3 end"
)

print(result.state)
```

Expected output:

```text
{'X': 2, 'Y': 6}
```

## CORE-05: Main CLI

Show help:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli --help
```

Check syntax:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli check examples/valid_loop.sipl
```

Parse source:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli parse examples/example01.sipl
```

Execute source:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/interpreter_demo.sipl
```

Trace execution:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli trace examples/valid_loop.sipl
```

Supply initial state:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/example01.sipl --state X=2 --state Y=3
```

JSON output is supported using `--json`.

## VIS-01: Concrete Syntax Tree

The concrete syntax tree includes grammar rules,
keywords, operators and punctuation.

Export all CST formats:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization examples/example01.sipl --format all --output output/example01
```

Supported formats:

- TXT
- JSON
- DOT
- SVG

## VIS-02: Abstract Syntax Tree

AST visualization uses the custom typed AST.

Generate all AST and comparison files:

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format all --output output/ast_example01
```

The command creates AST TXT, JSON, DOT and SVG,
as well as comparison JSON and HTML.

The HTML report displays CST and AST side by side.

## SEM-01: Semantic Term Generation

The semantic-term module recursively transforms
typed SIPL AST nodes into ASIPL algebraic terms.

It follows the notation of the Theory of Programming
practical handbook.

The implementation is located in:

`src/sipl/semantics/terms.py`

### Generate a Semantic Term

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl
```

The result uses semantic operators such as:

- AS^X: assignment
- S²: binary superposition
- S¹: unary superposition
- IF: conditional
- WH: while loop
- id: skip
- ·: sequential composition

### Generate JSON

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl --format json
```

The JSON document includes:

- schema_version
- notation
- term
- structure

The structure contains recursively nested
semantic operators and source coordinates.

### Export to a File

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl --format text --output output/example01.semantic.txt
```

### Python API

```python
from sipl.parser import parse_ast
from sipl.semantics import build_term, format_term

program = parse_ast("begin X := 5 end")

term = build_term(program)

print(format_term(term))
```

Expected output:

```text
AS^X(5̅)
```

### Semantic Scope

SEM-01 constructs formal semantic terms.

It does not evaluate the terms on a supplied state.
Program execution is implemented separately
in CORE-03.

Unary arithmetic minus uses an explicitly
documented extension named `uminus`.

## Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Run coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

Run semantic-term tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_semantics.py -v
```

Golden expected outputs are stored in:

`tests/golden/semantic_terms.json`

Verify CORE-03 coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_interpreter.py --cov=sipl.interpreter.runtime --cov-report=term-missing --cov-fail-under=80
```

## Documentation

- grammar/README.md
- docs/README.md
- examples/
- tests/

## Development Roadmap

1. CORE-01: Formal grammar
2. CORE-02: Typed AST
3. CORE-03: Interpreter
4. CORE-05: CLI and JSON
5. VIS-01: CST visualization
6. VIS-02: AST visualization and comparison
7. SEM-01: Semantic term generation
8. REL-02: GitHub Release

## Release

A tagged GitHub Release with release notes,
CHANGELOG and build artifacts will be prepared
for REL-02.

## References

Shyshatska O. V., Kryvolap A. V.,
Shyshatskyi A. V.

Theory of Programming. Practical Handbook, 2024.

Practical Work 2: Semantics and semantic terms.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

MIT License (planned; a LICENSE file will be
added before the public release).
