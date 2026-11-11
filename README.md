# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit for
SIPL (Simple Programming Language).

Developed for the "Theory of Programming" course.

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

The table shows the selected tasks, not the instructor's
final assessment.

## Implementation Status

### Implemented

- CORE-01: Formal SIPL grammar
- CORE-02: Parser and typed AST with SourceSpan
- CORE-03: Interpreter with runtime diagnostics
- CORE-05: CLI with parse, check, run and trace
- Structured JSON output and documented exit codes
- Automated unit and integration tests

### Planned

- VIS-01: Parse tree visualization
- VIS-02: AST visualization and comparison
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
│       │   ├── runtime.py
│       │   └── tracing.py
│       ├── semantics/
│       └── visualization/
├── examples/
├── tests/
│   ├── test_cli.py
│   ├── test_cli_integration.py
│   ├── test_interpreter.py
│   ├── test_parser.py
│   └── test_syntax.py
├── docs/
│   └── README.md
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

## Installation

### Prerequisites

- Python 3.11 or newer
- Windows PowerShell

### 1. Download

Download the repository as a ZIP archive using
GitHub's Code > Download ZIP.

Extract the archive and open its root folder
in VS Code.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## CLI Usage

All commands below are executed from the project root.

You can run the CLI using:

```powershell
.\.venv\Scripts\python.exe -m sipl.cli --help
```

Or use the installed `sipl` entry point:

```powershell
.\.venv\Scripts\sipl.exe --help
```

### Information

```powershell
.\.venv\Scripts\sipl.exe info
```

### Check syntax

```powershell
.\.venv\Scripts\sipl.exe check examples/valid_loop.sipl
```

### Parse to AST

```powershell
.\.venv\Scripts\sipl.exe parse examples/valid_loop.sipl
```

### Run a SIPL program

```powershell
.\.venv\Scripts\sipl.exe run examples/interpreter_demo.sipl
```

Expected final state:

```text
Result = 30
X = 0
```

### Trace execution

```powershell
.\.venv\Scripts\sipl.exe trace examples/valid_loop.sipl
```

The trace includes:

- Before and after statement events
- Step events
- Condition evaluations
- Variable changes
- Completion event

### Provide initial variables

```powershell
.\.venv\Scripts\sipl.exe run examples/example01.sipl --state X=2 --state Y=3
```

Expected result:

```text
R = 8
X = 2
Y = 0
```

### Set a step limit

```powershell
.\.venv\Scripts\sipl.exe run examples/valid_loop.sipl --max-steps 100
```

The default is 10000 execution steps.

## JSON Integration

The commands check, parse, run and trace support --json.

Example:

```powershell
.\.venv\Scripts\sipl.exe run examples/interpreter_demo.sipl --json
```

Successful responses use this envelope:

```json
{
  "schema_version": "1.0",
  "command": "run",
  "ok": true,
  "data": {
    "state": {
      "Result": 30,
      "X": 0
    },
    "steps": 18
  },
  "error": null
}
```

The same envelope is used for syntax and runtime errors.

Error responses contain:

- code
- message
- line
- column

The `parse` command includes a typed AST containing
node_type values and SourceSpan coordinates.

The `trace` command includes an ordered events array.

JSON is written to stdout. Diagnostic text for
non-JSON errors is written to stderr.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | SIPL syntax error |
| 2 | Invalid CLI arguments |
| 3 | SIPL runtime error |
| 4 | File reading error |

Invalid CLI arguments use argparse diagnostics.
The --json response envelope applies to successfully
parsed CLI arguments.

## SIPL Interpreter

The interpreter supports:

- Assignment
- Sequential execution
- If/then/else
- While/do
- Begin/end blocks
- Skip
- Integer arithmetic
- Boolean conditions

It uses explicit variable states and has a configurable
execution step limit.

## Python API

```python
from sipl.parser import parse_ast
from sipl.interpreter import run_source

program = parse_ast("begin X := 5 end")
result = run_source("begin X := 5 end")

print(type(program).__name__)
print(result.state)
```

Expected output:

```text
Program
{'X': 5}
```

## Examples

Valid SIPL programs:

- examples/example01.sipl
- examples/valid_condition.sipl
- examples/valid_loop.sipl
- examples/interpreter_demo.sipl

Invalid SIPL programs:

- examples/invalid_assignment.sipl
- examples/invalid_condition.sipl

## Testing

Run all automated tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run coverage analysis:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

Verify interpreter coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_interpreter.py --cov=sipl.interpreter.runtime --cov-report=term-missing --cov-fail-under=80
```

Integration tests launch the CLI as a separate
Python process and validate commands, JSON output,
diagnostics and exit codes.

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

MIT License (planned; license file will be added
before the first release).
