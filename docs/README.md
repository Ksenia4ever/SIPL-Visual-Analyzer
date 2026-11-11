# SIPL Visual Analyzer Documentation

## 1. Architecture

SIPL Visual Analyzer uses a modular architecture.

The current processing pipeline is:

SIPL Source Code
    |
    v
Lark Grammar
    |
    v
Concrete Parse Tree
    |
    v
AST Converter
    |
    v
Typed SIPL AST

The typed AST will be reused by the interpreter,
visualization tools and formal semantics modules.

## 2. Formal Grammar

The SIPL grammar is implemented in:

`src/sipl/grammar.lark`

It supports the core SIPL language constructs
defined in the Theory of Programming course.

Grammar documentation:

`grammar/README.md`

## 3. Syntax Analysis

Syntax validation is implemented in:

`src/sipl/syntax.py`

Available functions:

- parse_source(source)
- validate_source(source)
- validate_file(path)

The parser uses Lark with the LALR parsing algorithm.

Invalid programs produce SIPLSyntaxError exceptions
with source line and column information.

## 4. Typed Abstract Syntax Tree

The typed AST model is implemented in:

`src/sipl/ast.py`

AST conversion is implemented in:

`src/sipl/parser.py`

The AST does not depend on Lark data structures.

### Program

Program represents the root of a SIPL program.

It contains a statement representing the body.

### Statements

Supported statement nodes:

- Sequence
- Assignment
- IfStatement
- WhileStatement
- Block
- Skip

### Arithmetic Expressions

Supported expression nodes:

- IntegerLiteral
- Variable
- UnaryMinus
- BinaryExpression

BinaryExpression supports:

- Addition
- Subtraction
- Multiplication

### Boolean Conditions

Supported condition nodes:

- Comparison
- LogicalOr
- LogicalNot

Comparison supports equality and greater-than.

## 5. SourceSpan

Every AST node contains a SourceSpan object.

SourceSpan stores:

- start_line
- start_column
- end_line
- end_column
- start_pos
- end_pos

Line and column numbers are 1-based.

Character offsets are 0-based.

End positions are exclusive.

Source positions allow error reporting,
source highlighting and navigation.

Grouping parentheses are not represented as
independent AST nodes. Their source range is
included in the corresponding expression or
condition node.

## 6. Parser API

### parse_ast(source)

Converts SIPL source code into a typed Program AST.

Example:

```python
from sipl.parser import parse_ast

program = parse_ast("begin X := 5 end")
print(program)
```

### parse_ast_file(path)

Reads a SIPL file and returns its typed AST.

Example:

```python
from sipl.parser import parse_ast_file

program = parse_ast_file("examples/valid_loop.sipl")
print(program)
```

Both functions preserve syntax diagnostics from
the existing syntax analysis module.

## 7. Arithmetic Precedence

The executable grammar uses these priorities:

1. Parentheses
2. Unary minus
3. Multiplication
4. Addition and subtraction

For example:

2 + 3 * 4

is represented as:

2 + (3 * 4)

Arithmetic operators are stored explicitly
in BinaryExpression nodes.

## 8. Testing

Parser tests:

`tests/test_parser.py`

Tests verify:

- Program and statement nodes
- Assignments
- Arithmetic expressions
- Arithmetic precedence
- Conditions
- Loops
- Nested blocks
- Source positions
- Syntax errors
- File parsing

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## 9. Planned Modules

The typed AST will be used in:

- CORE-03: Interpreter
- CORE-05: CLI and JSON interface
- VIS-01: Parse tree visualization
- VIS-02: AST visualization
- SEM-01: Semantic term generation

## 10. Design Decisions

The AST consists of custom Python dataclasses.

AST nodes are immutable.

The parser separates concrete syntax from
semantic structure.

The SourceSpan model is shared across AST nodes.

The AST represents syntactic structure only.
Execution and evaluation will be implemented
in subsequent modules.
