# SIPL Visual Analyzer — Technical Documentation

## 1. Architecture

The project uses a modular architecture:

```text
SIPL source file
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
      +----------------+
      |                |
      v                v
  Interpreter      AST serializer
      |                |
      v                v
 State / Steps      JSON / Text
      |
      v
  Trace events
      |
      v
   CLI / JSON
```

The source grammar is located in:
`src/sipl/grammar.lark`

The typed AST is located in:
`src/sipl/ast.py`

The interpreter is located in:
`src/sipl/interpreter/runtime.py`

The tracing adapter is located in:
`src/sipl/interpreter/tracing.py`

The CLI is located in:
`src/sipl/cli.py`

## 2. Implemented Modules

### CORE-01

Formal SIPL grammar, lexical rules, positive
and negative syntax tests.

### CORE-02

Typed AST created from Lark's concrete parse tree.

Every AST node includes SourceSpan information.

### CORE-03

SIPL interpreter supporting assignment, sequence,
if, while, begin/end, skip, arithmetic expressions
and Boolean conditions.

Runtime errors include source coordinates.

An execution step limit prevents unlimited loops.

### CORE-05

Command-line interface with:

- check
- parse
- run
- trace

Commands support text output and structured JSON.

## 3. CLI Architecture

CLI arguments are processed using argparse.

The CLI reads a SIPL file, parses it into a
typed AST and invokes the corresponding service.

The CLI does not contain a separate SIPL parser
or interpreter.

## 4. JSON Contract

The current schema version is 1.0.

All JSON command responses use:

```json
{
  "schema_version": "1.0",
  "command": "check",
  "ok": true,
  "data": {
    "valid": true
  },
  "error": null
}
```

When a command fails:

- ok is false
- data is null
- error is an object

Error objects contain:

- code
- message
- line
- column

For file errors, line and column are null.

JSON field order is not semantically significant.

## 5. AST Serialization

The parse command recursively serializes
custom Python dataclasses.

Each AST node contains:

- node_type
- span
- node-specific attributes

SourceSpan contains:

- start_line
- start_column
- end_line
- end_column
- start_pos
- end_pos

Line and column coordinates are 1-based.

Character offsets are 0-based, with exclusive ends.

The JSON serializer does not expose raw Lark objects.

## 6. Execution State

The run command returns:

- state: final variable values
- steps: execution step count

Initial variables may be supplied using:

--state NAME=INTEGER

The option can be repeated for different variables.

## 7. Trace Contract

The trace command uses TracingInterpreter,
which extends the shared Interpreter class.

Execution events contain:

- event_id
- type
- step
- line
- column
- state

Additional fields depend on event type.

Supported event types:

- before_statement
- step
- condition_evaluated
- variable_changed
- after_statement
- completed

variable_changed also includes:

- name
- old_value
- new_value

condition_evaluated also includes:

- result

The trace follows actual program execution.
It is not generated from a static example.

A trace result is returned only after successful
execution. Runtime errors produce an error response.

## 8. Exit Codes

0: Success

1: SIPL syntax error

2: CLI argument error

3: SIPL runtime error

4: File reading error

Unknown commands and malformed options are handled
by argparse and produce exit code 2.

## 9. Testing

Unit tests cover grammar parsing, AST and execution.

Integration tests cover the command-line interface
through subprocess execution.

Integration tests validate:

- Exit codes
- Text output
- JSON output
- AST serialization
- Execution results
- Runtime errors
- Trace events
- Initial variables
- Invalid arguments
- File errors

Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## 10. Future Modules

The existing APIs will be reused for:

- VIS-01: Parse tree visualization
- VIS-02: AST visualization
- SEM-01: Semantic term generation

The next visualization modules must generate
their results from actual parse trees and AST nodes,
not from hardcoded examples.
