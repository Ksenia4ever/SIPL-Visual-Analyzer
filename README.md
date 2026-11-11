# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit
for the SIPL (Simple Programming Language).

The project is developed for the
"Theory of Programming" course.

## Project Goal

The goal is to create a modular toolkit for parsing,
executing, visualizing and analyzing SIPL programs.

The project follows the architecture described in
the SIPL Language Toolkit coursework specification.

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

The table describes the selected project scope,
not the total number of completed tasks.

## Implementation Status

### Completed

- Project initialization
- Python package structure
- Basic CLI with info and version commands
- CORE-01: Formal SIPL Grammar
- Syntax validation
- Error location reporting
- Positive and negative syntax tests

### Planned

- CORE-02: Parser and typed AST
- CORE-03: Interpreter
- CORE-05: Full CLI and JSON mode
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
│       ├── cli.py
│       ├── grammar.lark
│       ├── syntax.py
│       ├── interpreter/
│       ├── semantics/
│       └── visualization/
├── examples/
├── tests/
│   ├── test_cli.py
│   └── test_syntax.py
├── docs/
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

## Installation

### Prerequisites

- Python 3.11 or newer
- Windows PowerShell

### 1. Download the Project

Download the project archive from GitHub using:

Code > Download ZIP

Extract it and open the project folder in VS Code.

### 2. Create a Virtual Environment

Open PowerShell in the project directory:

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

Show information:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli info
```

The CLI commands parse, check, run and trace
will be added during later stages.

## Syntax Validation

The syntax module provides three functions:

- parse_source(source)
- validate_source(source)
- validate_file(path)

Example:

```python
from sipl.syntax import validate_source

source = "begin X := 5 end"

print(validate_source(source))
```

Expected output:

```text
True
```

Invalid example:

```python
from sipl.syntax import validate_source

source = "begin X = 5 end"

print(validate_source(source))
```

Expected output:

```text
False
```

The grammar is located in:

`src/sipl/grammar.lark`

Detailed grammar documentation:

`grammar/README.md`

## Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run coverage analysis:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

The CORE-03 module requires at least 80% coverage
of the language core.

This criterion will be verified after implementation
of the interpreter.

## SIPL Examples

Valid examples:

- examples/example01.sipl
- examples/valid_condition.sipl
- examples/valid_loop.sipl

Invalid examples:

- examples/invalid_assignment.sipl
- examples/invalid_condition.sipl

## Development Roadmap

1. Formal grammar - CORE-01
2. Parser and typed AST - CORE-02
3. Interpreter - CORE-03
4. CLI and JSON output - CORE-05
5. Parse tree visualization - VIS-01
6. AST visualization - VIS-02
7. Formal semantics - SEM-01
8. Release and documentation - REL-02

## Documentation

- grammar/README.md
- docs/
- examples/
- tests/

## Release

The project uses Semantic Versioning.

A tagged GitHub Release with notes, CHANGELOG
and build artifacts will be prepared for REL-02.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

MIT License (planned; license file will be added
before the first public release).
