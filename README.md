# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit
for SIPL (Simple Programming Language).

The project is developed for the
"Theory of Programming" course.

## Project Goal

The goal is to create a modular toolkit for parsing,
executing, visualizing and analyzing SIPL programs.

The project follows the SIPL Language Toolkit
coursework specification.

## Selected Tasks

| Task ID | Description | Points |
|---------|-------------|--------|
| CORE-01 | Formal SIPL Grammar | 0.5 |
| CORE-02 | Parser and Typed AST | 1.5 |
| CORE-03 | SIPL Interpreter | 2.0 |
| CORE-05 | Command-Line Interface | 1.0 |
| VIS-01 | Parse Tree Visualization | 1.5 |
| VIS-02 | AST Visualization | 1.0 |
| SEM-01 | Semantic Term Generation | 2.0 |
| REL-02 | GitHub Release | 0.5 |
| **Total** | | **10.0** |

The table represents the selected project scope,
not the number of tasks accepted by the instructor.

## Implementation Status

### Implemented

- Project initialization
- Python package structure
- Basic CLI
- CORE-01: Formal SIPL grammar
- Syntax validation and error diagnostics
- Positive and negative grammar tests
- CORE-02: Typed AST
- Conversion from Lark parse trees to AST
- SourceSpan for AST nodes
- AST parser tests

### Planned

- CORE-03: Interpreter
- CORE-05: Full CLI and JSON interface
- VIS-01: Parse tree visualization
- VIS-02: AST visualization
- SEM-01: Semantic term generation
- REL-02: GitHub Release

## Technologies

- Python 3.11+
- Lark
- pytest
- pytest-cov
- Graphviz (planned)
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
│       ├── semantics/
│       └── visualization/
├── examples/
├── tests/
│   ├── test_cli.py
│   ├── test_parser.py
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

### 1. Download the Project

Download the project ZIP archive from GitHub
using Code > Download ZIP.

Extract the archive and open the project folder
in Visual Studio Code.

### 2. Create a Virtual Environment

Open PowerShell in the project directory.

```powershell
py -m venv .venv
```

### 3. Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## CLI Usage

Show help:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli --help
```

Show version:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli --version
```

Show project information:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli info
```

Full parse, check, run and trace commands
will be implemented during later stages.

## Syntax Validation

The syntax module provides:

- parse_source(source)
- validate_source(source)
- validate_file(path)

Example:

```python
from sipl.syntax import validate_source

print(validate_source("begin X := 5 end"))
```

Expected output:

```text
True
```

Invalid example:

```python
from sipl.syntax import validate_source

print(validate_source("begin X = 5 end"))
```

Expected output:

```text
False
```

## Typed AST

The AST model is implemented in:

`src/sipl/ast.py`

The AST converter is implemented in:

`src/sipl/parser.py`

Example:

```python
from sipl.parser import parse_ast

source = "begin X := 2 + 3 * 4 end"

program = parse_ast(source)

print(type(program).__name__)
print(type(program.body).__name__)
```

Expected output:

```text
Program
Sequence
```

The AST uses custom dataclasses and contains
source position information through SourceSpan.

The parser supports assignments, sequences,
conditionals, loops, blocks, arithmetic expressions
and Boolean conditions.

## SIPL Examples

Valid examples:

- examples/example01.sipl
- examples/valid_condition.sipl
- examples/valid_loop.sipl

Invalid examples:

- examples/invalid_assignment.sipl
- examples/invalid_condition.sipl

## Automated Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run with coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

Tests include:

- CLI tests
- Positive grammar tests
- Negative grammar tests
- Syntax error tests
- AST structure tests
- SourceSpan tests

The CORE-03 interpreter requires at least
80% test coverage of the language core.

This criterion will be verified after
the interpreter is implemented.

## Documentation

- grammar/README.md
- docs/README.md
- examples/
- tests/

## Development Roadmap

1. CORE-01: Formal grammar
2. CORE-02: Typed AST
3. CORE-03: Interpreter
4. CORE-05: CLI and JSON output
5. VIS-01: Parse tree visualization
6. VIS-02: AST visualization
7. SEM-01: Formal semantic terms
8. REL-02: GitHub Release

## Release

The project follows the Semantic Versioning approach.

A tagged release with release notes, a changelog
and build artifacts will be prepared for REL-02.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

MIT License (planned; the license file will
be added before the public release).
