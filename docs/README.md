# SIPL Visual Analyzer — Technical Documentation

## 1. Architecture

The project has the following processing pipeline:

```text
SIPL source
    |
    v
Lark grammar
    |
    +------------------+
    |                  |
    v                  v
   CST             Typed AST
    |                  |
    v                  +---- Interpreter
VIS-01                 |
    |                  +---- VIS-02
    |                  |
    |                  +---- SEM-01
    |                           |
    v                           v
CST diagrams               Semantic terms
```

## 2. Completed Core Modules

### CORE-01

Formal SIPL grammar and syntax validation.

### CORE-02

Typed AST with source positions.

### CORE-03

Interpreter for the base SIPL language.

### CORE-05

Command-line interface with check, parse,
run, trace and JSON output.

## 3. Visualization Modules

### VIS-01

Concrete syntax-tree visualization using
the original Lark grammar.

Supported formats:

- TXT
- JSON
- DOT
- SVG

### VIS-02

Abstract syntax-tree visualization using
the custom AST data model.

Includes a side-by-side HTML comparison
of CST and AST.

## 4. SEM-01: Formal Semantics

Implementation:

`src/sipl/semantics/terms.py`

Command-line entry point:

`src/sipl/semantics/__main__.py`

SEM-01 constructs formal semantic terms
recursively from typed AST nodes.

The notation follows the practical handbook
for the Theory of Programming course.

## 5. Semantic Transformation Rules

Program:

sem_P(begin S end) = sem_S(S)

Assignment:

sem_S(X := a) = AS^X(sem_A(a))

Sequence:

sem_S(S1; S2) = sem_S(S1) · sem_S(S2)

Conditional:

sem_S(if b then S1 else S2)
    = IF(sem_B(b), sem_S(S1), sem_S(S2))

While loop:

sem_S(while b do S)
    = WH(sem_B(b), sem_S(S))

Block:

sem_S(begin S end) = sem_S(S)

Skip:

sem_S(skip) = id

Arithmetic:

sem_A(a1 + a2)
    = S²(add, sem_A(a1), sem_A(a2))

sem_A(a1 - a2)
    = S²(sub, sem_A(a1), sem_A(a2))

sem_A(a1 * a2)
    = S²(mult, sem_A(a1), sem_A(a2))

Comparison:

sem_B(a1 = a2)
    = S²(eq, sem_A(a1), sem_A(a2))

sem_B(a1 > a2)
    = S²(gr, sem_A(a1), sem_A(a2))

Boolean operators:

sem_B(b1 ∨ b2)
    = S²(or, sem_B(b1), sem_B(b2))

sem_B(¬b)
    = S¹(neg, sem_B(b))

Constants and variables are represented
as constant functions and dereferencing functions.

Unary arithmetic minus is implemented as
S¹(uminus, sem_A(a)), a documented extension.

## 6. SemanticTerm Structure

Each semantic term contains:

- symbol
- arguments
- value
- span

The node is immutable.

Nested terms are stored recursively.

SourceSpan preserves the relationship
between semantic terms and AST nodes.

## 7. Text Representation

The formatting module supports:

- AS^X
- S²
- S¹
- IF
- WH
- id
- Sequential composition ·

Constant functions use an overlined
numeric representation.

Variable dereferencing uses the ⇒ symbol.

## 8. JSON Representation

JSON output contains:

- schema_version
- notation
- term
- structure

The structure is recursively serialized
from SemanticTerm objects.

Every node contains a source span when
it originates from an AST node.

## 9. Golden Tests

Golden test data:

`tests/golden/semantic_terms.json`

Test module:

`tests/test_semantics.py`

The tests compare actual generated terms
with predetermined expected representations.

The examples cover all base SIPL constructs,
as well as documented unary-minus support.

The example from Practical Work 2
is included in the golden test suite.

## 10. SEM-01 Command Line

Show help:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics --help
```

Generate a term:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl
```

Generate JSON:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl --format json
```

Save a term:

```powershell
.\.venv\Scripts\python.exe -m sipl.semantics examples/example01.sipl --output output/semantic.txt
```

Return codes:

- 0: Success
- 1: Syntax error
- 2: Invalid CLI arguments
- 4: File error
- 5: Semantic construction error

## 11. Scope

SEM-01 generates formal terms and does
not evaluate them on an initial state.

Evaluation of semantic terms is a separate
coursework task.

## 12. Verification

Run semantic tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_semantics.py -v
```

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Check coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=sipl --cov-report=term-missing
```

## 13. References

O. V. Shyshatska, A. V. Kryvolap,
A. V. Shyshatskyi.

Theory of Programming. Practical Handbook, 2024.

Practical Work 2, pages 13–18.

M. S. Nikitchenko.

Theory of Programming, 2020.
