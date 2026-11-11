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

The table describes the selected project scope,
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
- SourceSpan for AST nodes
- Lark-to-AST conversion
- CORE-03: SIPL interpreter
- Assignment and sequence execution
- Conditional statements and loops
- Arithmetic and Boolean expressions
- Initial and final variable states
- Execution step limit
- Runtime diagnostics
- Automated interpreter tests

### Planned

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
│       │   ├── __init__.py
│       │   └── runtime.py
│       ├── semantics/
│       └── visualization/
├── examples/
│   ├── example01.sipl
│   ├── valid_condition.sipl
│   ├── valid_loop.sipl
│   ├── invalid_assignment.sipl
│   ├── invalid_condition.sipl
│   └── interpreter_demo.sipl
├── tests/
│   ├── test_cli.py
│   ├── test_syntax.py
│   ├── test_parser.py
│   └── test_interpreter.py
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

Download the project archive from GitHub
using Code > Download ZIP.

Extract it and open the project directory
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
will be added in CORE-05.

## Syntax Validation

Available functions:

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

## Typed AST

AST classes are implemented in:

`src/sipl/ast.py`

AST parsing is implemented in:

`src/sipl/parser.py`

Example:

```python
from sipl.parser import parse_ast

program = parse_ast("begin X := 5 end")

print(type(program).__name__)
```

Expected output:

```text
Program
```

Each AST node contains a SourceSpan.

## SIPL Interpreter

The interpreter is implemented in:

`src/sipl/interpreter/`

It supports:

- Assignment
- Sequential composition
- If/then/else
- While/do
- Begin/end blocks
- Skip
- Integer arithmetic
- Boolean conditions

### Execute SIPL Source

```python
from sipl.interpreter import run_source

result = run_source(
    "begin X := 2; Y := X * 3 end"
)

print(result.state)
print(result.steps)
```

Expected output:

```text
{'X': 2, 'Y': 6}
2
```

### Execute a SIPL File

```python
from sipl.interpreter import run_file

result = run_file(
    "examples/interpreter_demo.sipl"
)

print(result.state)
```

Expected output:

```text
{'X': 0, 'Result': 30}
```

### Initial Variable State

```python
from sipl.interpreter import run_source

result = run_source(
    "begin R := X * 2 end",
    initial_state={"X": 5},
)

print(result.state)
```

Expected output:

```text
{'X': 5, 'R': 10}
```

### Execution Step Limit

The default limit is 10000 execution steps.

It can be changed:

```python
from sipl.interpreter import run_source

result = run_source(
    "begin X := 5 end",
    max_steps=100,
)
```

The interpreter raises StepLimitExceededError
when the limit is exceeded.

Reading an undefined variable raises
UndefinedVariableError.

Runtime errors include source positions.

## SIPL Examples

Valid programs:

- examples/example01.sipl
- examples/valid_condition.sipl
- examples/valid_loop.sipl
- examples/interpreter_demo.sipl

Invalid programs:

- examples/invalid_assignment.sipl
- examples/invalid_condition.sipl

## Automated Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run general coverage analysis:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

Verify CORE-03 interpreter coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_interpreter.py --cov=sipl.interpreter --cov-report=term-missing --cov-fail-under=80
```

CORE-03 requires at least 80% interpreter
coverage and protection against infinite loops.

The test suite checks both normal execution
and runtime error scenarios.

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

The project follows Semantic Versioning.

A tagged GitHub Release with release notes,
CHANGELOG and build artifacts will be prepared
for REL-02.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

MIT License (planned; the license file
will be added before the public release).
