# SIPL Visual Analyzer

SIPL Visual Analyzer is an educational Python toolkit
for the SIPL (Simple Programming Language).

The project is developed for the
"Theory of Programming" course.

## Project Goal

The goal is to implement a modular toolkit for parsing,
executing, visualizing and analyzing SIPL programs.

The project follows the modular architecture described
in the SIPL Language Toolkit coursework specification.

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

The selected tasks represent the planned scope of the
project. This table is not a completion claim.

## Current Status

Stage 1: Project initialization.

Currently implemented:

- Python package structure
- Basic CLI with info and version commands
- Initial automated CLI tests
- Example SIPL program

The grammar, parser, interpreter, visualization and
semantic modules will be implemented in later stages.

## Technologies

- Python 3.11+
- Lark
- pytest
- pytest-cov
- Graphviz (planned for visualization)
- Git and GitHub

## Project Structure

```text
SIPL-Visual-Analyzer/
├── grammar/
├── src/
│   └── sipl/
│       ├── cli.py
│       ├── interpreter/
│       ├── semantics/
│       └── visualization/
├── examples/
├── tests/
├── docs/
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

## Installation

### Prerequisites

- Python 3.11 or newer
- Git

### 1. Clone the repository

```powershell
git clone <YOUR_REPOSITORY_URL>
cd SIPL-Visual-Analyzer
```

Replace `<YOUR_REPOSITORY_URL>` with the actual repository
URL after publication.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

### 3. Install dependencies

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Basic Usage

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

The final CLI will also support:

- parse
- check
- run
- trace

These commands are not implemented yet.

## Testing

Run automated tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run tests with coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

The CORE-03 task requires at least 80% test coverage
of the implemented language core.

This requirement will be checked after the interpreter
is implemented.

## SIPL Example

```text
begin
    R := 1;
    while Y > 0 do
    begin
        R := R * X;
        Y := Y - 1
    end
end
```

The example program is located in:

`examples/example01.sipl`

## Documentation

Additional documentation is available in:

- grammar/
- docs/
- examples/
- tests/

## Release

The project plans to use Semantic Versioning.

REL-02 requires a tagged GitHub release with release notes,
a changelog and build artifacts.

## Course

Theory of Programming

SIPL Language Toolkit Coursework

## License

MIT License (planned; license file to be added before release).
