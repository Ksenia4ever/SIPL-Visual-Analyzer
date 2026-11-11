# Changelog

All notable changes to SIPL Visual Analyzer are documented here.

The project follows Semantic Versioning.

## [1.0.0] - 2026-11-11

### Added

#### CORE-01 — Formal Grammar
- Machine-readable SIPL grammar using Lark
- Lexical rules and syntax validation
- Positive and negative grammar tests
- Syntax diagnostics with source positions

#### CORE-02 — Typed AST
- Custom typed AST using immutable Python dataclasses
- SourceSpan metadata for AST nodes
- Lark-to-AST conversion
- Parser tests

#### CORE-03 — Interpreter
- SIPL assignment and sequential execution
- If/then/else and while loops
- Begin/end and skip statements
- Arithmetic and Boolean expressions
- Variable state management
- Runtime diagnostics
- Execution step limit

#### CORE-05 — CLI
- Check, parse, run and trace commands
- Structured JSON output
- Documented exit codes
- Initial state arguments
- Source-linked execution trace
- CLI integration tests

#### VIS-01 — CST Visualization
- Concrete syntax tree generation
- Text, JSON, DOT and SVG export
- Source coordinates for grammar nodes
- Graphviz rendering

#### VIS-02 — AST Visualization
- Typed AST visualization
- AST Text, JSON, DOT and SVG export
- CST/AST comparison statistics
- Side-by-side HTML comparison
- Source-linked AST nodes

#### SEM-01 — Formal Semantics
- Recursive semantic-term construction
- ASIPL course notation
- Text and JSON term export
- Golden semantic-term tests
- Example from the Theory of Programming handbook

#### REL-02 — Release
- Semantic Versioning
- MIT License
- Source distribution and wheel packaging
- Release documentation
- GitHub tagged release preparation

### Quality Assurance
- Automated unit and integration tests
- Golden tests for formal semantics
- Coverage verification for the interpreter
- Build and distribution verification

## [0.1.0] - 2026-11-11

### Added
- Initial Python project structure
- Python package configuration
- Basic CLI with info and version commands
- Initial CLI tests
- Initial SIPL example
- Documentation structure
