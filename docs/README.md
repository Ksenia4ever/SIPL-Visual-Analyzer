# SIPL Visual Analyzer — Technical Documentation

## 1. Architecture

SIPL Visual Analyzer uses a modular architecture.

The current processing pipeline is:

```text
SIPL source
    |
    v
Lark grammar
    |
    v
Concrete parse tree
    |
    v
Typed AST
    |
    v
SIPL interpreter
    |
    v
ExecutionResult
```

The interpreter reuses the parser and AST from
CORE-01 and CORE-02.

No separate parser is implemented inside the
execution engine.

## 2. Formal Grammar

The grammar is located in:

`src/sipl/grammar.lark`

Detailed language specification:

`grammar/README.md`

The supported language includes:

- Assignment
- Sequential composition
- If/then/else
- While/do
- Begin/end
- Skip
- Integer arithmetic
- Boolean conditions

## 3. Syntax and AST

Syntax validation:

`src/sipl/syntax.py`

Typed AST models:

`src/sipl/ast.py`

AST transformation:

`src/sipl/parser.py`

Every AST node contains SourceSpan information
for source position tracking.

## 4. Interpreter

The interpreter is implemented in:

`src/sipl/interpreter/runtime.py`

Public API:

`src/sipl/interpreter/__init__.py`

Main classes:

- Interpreter
- ExecutionResult
- SIPLRuntimeError
- UndefinedVariableError
- StepLimitExceededError

Main functions:

- run_source()
- run_file()
- run_ast()

## 5. Execution State

The interpreter uses a dictionary that maps
variable names to integer values.

Example:

```python
{
    "X": 5,
    "Result": 10
}
```

An initial state may be supplied by the caller.

Example:

```python
from sipl.interpreter import run_source

source = "begin R := X * 2 end"

result = run_source(
    source,
    initial_state={"X": 5},
)

print(result.state)
```

Expected output:

```text
{'X': 5, 'R': 10}
```

Variables are not automatically initialized.

Reading an undefined variable raises
UndefinedVariableError.

## 6. Statement Semantics

### Assignment

The expression is evaluated and its value is
assigned to the specified variable.

### Sequence

Statements are executed from left to right.

### Conditional

The Boolean condition determines which branch
is executed.

### While

The condition is evaluated before every iteration.

When the condition becomes false, execution
continues after the loop.

### Block

A begin/end block executes its contained statements.

Blocks do not introduce a separate variable scope.

### Skip

Skip performs no state modification.

## 7. Arithmetic Expressions

Supported operations:

- Addition
- Subtraction
- Multiplication
- Unary minus

Arithmetic uses Python arbitrary-precision integers.

Division is not part of the base SIPL grammar.

## 8. Boolean Conditions

Supported operations:

- Equality
- Greater-than
- Logical OR
- Logical NOT

Logical OR uses short-circuit evaluation.

## 9. Step Limit

The default execution limit is 10000 steps.

A step is counted for:

- Assignment
- Skip
- If condition evaluation
- While condition evaluation

The final false while check is also counted.

Sequence and Block nodes are structural wrappers
and do not consume an additional step.

When the limit is exceeded, the interpreter raises
StepLimitExceededError.

Example:

```python
from sipl.interpreter import run_source

run_source(
    "begin X := 1; while X > 0 do skip end",
    max_steps=10,
)
```

The interpreter stops execution rather than
continuing indefinitely.

## 10. Error Handling

Syntax errors:

SIPLSyntaxError

Runtime errors:

SIPLRuntimeError

Specialized runtime errors:

- UndefinedVariableError
- StepLimitExceededError

Runtime errors contain the corresponding SourceSpan
and a human-readable position.

When execution raises an error, no successful
ExecutionResult is returned.

## 11. ExecutionResult

The result contains:

- state: final variable values
- steps: number of execution steps

Example:

```python
from sipl.interpreter import run_source

result = run_source("begin X := 5 end")

print(result.state)
print(result.steps)
```

Expected output:

```text
{'X': 5}
1
```

## 12. Testing

Tests are located in:

- tests/test_cli.py
- tests/test_syntax.py
- tests/test_parser.py
- tests/test_interpreter.py

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Check interpreter coverage:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_interpreter.py --cov=sipl.interpreter --cov-report=term-missing --cov-fail-under=80
```

CORE-03 requires at least 80% coverage
of the interpreter implementation.

## 13. Current Limitations

The current interpreter supports the basic
SIPL language from the course.

Not implemented yet:

- Full CLI run/check/trace commands
- Structured JSON results
- Execution trace visualization
- Parse tree and AST visualization
- Formal semantic terms
- Recursive function extensions

These capabilities belong to later stages
or additional modules.

## 14. Planned Integration

The existing interpreter API will be reused by:

- CORE-05: CLI and JSON interface
- VIS modules: visualization
- SEM-01: semantic analysis

This prevents duplication of the execution engine.
