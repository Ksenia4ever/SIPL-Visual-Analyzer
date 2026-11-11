# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit
for SIPL (Simple Programming Language).

Developed for the Theory of Programming course.

## Project Goal

The project provides a modular toolkit for parsing,
executing, visualizing and analyzing SIPL programs.

It follows the SIPL Language Toolkit coursework
specification.

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

The points represent the selected coursework tasks,
not the instructor's final assessment.

## Implementation Status

### Implemented

- CORE-01: SIPL grammar and syntax validation
- CORE-02: Typed AST and SourceSpan
- CORE-03: SIPL interpreter
- CORE-05: CLI and JSON interface
- VIS-01: CST visualization
- VIS-02: AST visualization and CST/AST comparison

### Planned

- SEM-01: Formal semantic term generation
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
│       └── visualization/
│           ├── __init__.py
│           ├── __main__.py
│           ├── tree.py
│           ├── ast_tree.py
│           └── ast_cli.py
├── examples/
├── tests/
│   ├── test_cli.py
│   ├── test_cli_integration.py
│   ├── test_interpreter.py
│   ├── test_parser.py
│   ├── test_parse_tree_visualization.py
│   ├── test_ast_visualization.py
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
- Graphviz for SVG and HTML comparison

### 1. Download the Project

Download the project using GitHub's
Code > Download ZIP feature.

Extract the archive and open it in VS Code.

### 2. Create a Virtual Environment

```powershell
py -m venv .venv
```

### 3. Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### 4. Install Graphviz

```powershell
winget install --id Graphviz.Graphviz -e
```

Restart the terminal and check:

```powershell
dot -V
```

## Main CLI

### Help

```powershell
.\.venv\Scripts\python.exe -m sipl.cli --help
```

### Check Syntax

```powershell
.\.venv\Scripts\python.exe -m sipl.cli check examples/valid_loop.sipl
```

### Parse to Typed AST

```powershell
.\.venv\Scripts\python.exe -m sipl.cli parse examples/valid_loop.sipl
```

### Execute a Program

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/interpreter_demo.sipl
```

Expected final state:

```text
Result = 30
X = 0
```

### Trace Execution

```powershell
.\.venv\Scripts\python.exe -m sipl.cli trace examples/valid_loop.sipl
```

### Initial Variable Values

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/example01.sipl --state X=2 --state Y=3
```

### JSON Output

```powershell
.\.venv\Scripts\python.exe -m sipl.cli run examples/interpreter_demo.sipl --json
```

## VIS-01: CST Visualization

The concrete syntax tree is generated
from the original SIPL grammar using Lark.

CST includes grammar rules, keywords and punctuation.

It provides Text, JSON, DOT and SVG exports.

### Text

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization examples/example01.sipl --format text
```

### All Formats

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization examples/example01.sipl --format all --output output/example01
```

## VIS-02: AST Visualization

The AST is generated from the custom typed
nodes implemented in CORE-02.

Every AST node includes a SourceSpan.

The AST visualization shows:

- Node types
- Attributes and operators
- Parent-child relationships
- Source positions
- Field names on edges

### Text AST

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format text
```

### JSON AST

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format json
```

### DOT AST

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format dot --output output/example01.ast.dot
```

### SVG AST

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format svg --output output/example01.ast.svg
```

## CST vs AST Comparison

VIS-02 provides an HTML page containing
both concrete and abstract syntax trees.

The page includes:

- CST diagram
- AST diagram
- Number of CST nodes
- Number of AST nodes
- Number of CST terminal tokens
- Original SIPL source code

### Generate HTML Comparison

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format compare --output output/example01.comparison.html
```

### Generate Comparison JSON

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format compare-json
```

### Generate All VIS-02 Files

```powershell
.\.venv\Scripts\python.exe -m sipl.visualization.ast_cli examples/example01.sipl --format all --output output/ast_example01
```

The last command creates:

- example01.ast.txt
- example01.ast.json
- example01.ast.dot
- example01.ast.svg
- example01.comparison.json
- example01.comparison.html

The comparison uses real CST and AST structures.

No visualized program structure is hardcoded.

## CST and AST Differences

CST preserves the exact grammar structure,
including terminal symbols such as begin,
end, semicolons and assignment operators.

AST preserves the semantic program structure
using typed nodes such as Program, Assignment,
WhileStatement, BinaryExpression and Variable.

AST usually contains fewer nodes.

Both representations preserve source positions.

## Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run tests with coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

Run VIS-02 tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_ast_visualization.py -v
```

Verify CORE-03 interpreter coverage:

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
7. SEM-01: Formal semantic terms
8. REL-02: GitHub Release

## Release

A tagged GitHub Release with notes, CHANGELOG
and artifacts will be prepared for REL-02.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

MIT License (planned; license file will
be added before the public release).
