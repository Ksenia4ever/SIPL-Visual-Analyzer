# SIPL Formal Grammar

## 1. Purpose

This document describes the formal syntax and lexical
rules of the SIPL (Simple Programming Language).

The implementation follows the SIPL language used in
the Theory of Programming course.

The executable grammar is stored in:

`src/sipl/grammar.lark`

The grammar is implemented using Lark.

## 2. Language Overview

SIPL is a simplified imperative programming language.

It supports:

- Integer variables and constants
- Arithmetic expressions
- Assignment
- Sequential composition
- Conditional statements
- While loops
- Begin/end blocks
- Skip statements

SIPL does not provide input/output statements,
procedures, or complex data types in its basic version.

## 3. Course BNF

The basic program structure is:

```text
<program> ::= begin <statement> end
```

Statements:

```text
<statement> ::=
      <variable> := <expression>
    | <statement> ; <statement>
    | if <condition> then <statement>
      else <statement>
    | while <condition> do <statement>
    | begin <statement> end
    | skip
```

Arithmetic expressions:

```text
<expression> ::=
      <number>
    | <variable>
    | <expression> + <expression>
    | <expression> - <expression>
    | <expression> * <expression>
    | ( <expression> )
```

Conditions:

```text
<condition> ::=
      <expression> = <expression>
    | <expression> > <expression>
    | <condition> ∨ <condition>
    | ¬ <condition>
    | ( <condition> )
```

## 4. Lexical Specification

### Identifiers

An identifier starts with a Latin letter.

It can contain:

- Latin letters
- Digits
- Underscores

Examples:

```text
X
Y
Result
counter1
total_sum
```

Identifiers are case-sensitive.

The following words are reserved for language constructs:

```text
begin
end
if
then
else
while
do
skip
```

### Integer constants

Non-negative integer constants are represented by
sequences of decimal digits.

Negative integer values use unary minus.

Examples:

```text
0
5
123
-7
```

### Assignment

The assignment operator is:

```text
:=
```

Example:

```text
X := 5
```

### Arithmetic operators

```text
+
-
*
```

Division is not included in the basic SIPL grammar.

### Comparison operators

```text
=
>
```

Other comparison operators are not supported by
this implementation.

### Logical operators

```text
∨
¬
```

The OR operator is represented by the Unicode symbol
U+2228.

The NOT operator is represented by the Unicode symbol
U+00AC.

### Delimiters

```text
;
(
)
```

Whitespace and line breaks are ignored where
permitted by the grammar.

Comments are not part of the implemented SIPL syntax.

## 5. Parsing and Precedence

The original course BNF is a theoretical description
that can be ambiguous for some expressions and nested
statements.

The executable Lark grammar fixes parsing conventions.

Arithmetic precedence:

1. Parentheses
2. Unary minus
3. Multiplication
4. Addition and subtraction

Boolean precedence:

1. Parentheses
2. Logical NOT
3. Logical OR

Statement sequences are separated by semicolons.

To use multiple statements inside the body of an
if or while statement, use a begin/end block.

The else branch is associated with the nearest
unmatched if statement.

The executable grammar is the authoritative syntax
specification for this implementation.

## 6. Valid Programs

Basic assignment:

```text
begin
    X := 5
end
```

Conditional statement:

```text
begin
    if X > 0 then
        Y := 1
    else
        Y := 0
end
```

While loop:

```text
begin
    while X > 0 do
    begin
        X := X - 1
    end
end
```

## 7. Invalid Programs

Incorrect assignment:

```text
begin
    X = 5
end
```

Missing else:

```text
begin
    if X > 0 then skip
end
```

Unsupported division:

```text
begin
    X := 10 / 2
end
```

## 8. Validation

Syntax validation is implemented in:

`src/sipl/syntax.py`

Main functions:

- parse_source()
- validate_source()
- validate_file()

Syntax errors contain source line and column
information when provided by the parser.

The parser returns a Lark concrete parse tree.
The custom typed AST belongs to CORE-02.

## 9. Automated Tests

Tests are located in:

`tests/test_syntax.py`

The test suite contains:

- 12 positive grammar cases
- 14 negative grammar cases
- Parse tree validation
- Error location validation
- File validation
- Parser caching validation

Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## 10. Limitations

This version supports the basic SIPL language.

It does not support:

- Division
- Boolean AND
- Other comparison operators
- Input/output instructions
- Procedures
- Recursive functions
- User-defined functions

Some ambiguity from the theoretical BNF is resolved
by explicit parsing conventions.

Additional language constructs must be documented
as separate extensions.

## 11. References

O. V. Shyshatska, A. V. Kryvolap, A. V. Shyshatskyi.

Theory of Programming. Practical Handbook, 2024.

Practical Work 1: SIPL syntax and BNF.

SIPL Language Toolkit Coursework Specification, 2026.
