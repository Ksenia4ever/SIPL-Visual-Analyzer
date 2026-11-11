"""Typed AST nodes and source positions for the SIPL language."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceSpan:
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    start_pos: int
    end_pos: int


@dataclass(frozen=True, kw_only=True)
class Node:
    span: SourceSpan


@dataclass(frozen=True)
class Statement(Node):
    pass


@dataclass(frozen=True)
class Expression(Node):
    pass


@dataclass(frozen=True)
class Condition(Node):
    pass


@dataclass(frozen=True)
class Program(Node):
    body: Statement


# Statements

@dataclass(frozen=True)
class Sequence(Statement):
    statements: tuple[Statement, ...]


@dataclass(frozen=True)
class Assignment(Statement):
    name: str
    value: Expression


@dataclass(frozen=True)
class IfStatement(Statement):
    condition: Condition
    then_branch: Statement
    else_branch: Statement


@dataclass(frozen=True)
class WhileStatement(Statement):
    condition: Condition
    body: Statement


@dataclass(frozen=True)
class Block(Statement):
    body: Statement


@dataclass(frozen=True)
class Skip(Statement):
    pass


# Arithmetic expressions

@dataclass(frozen=True)
class IntegerLiteral(Expression):
    value: int


@dataclass(frozen=True)
class Variable(Expression):
    name: str


@dataclass(frozen=True)
class UnaryMinus(Expression):
    operand: Expression


@dataclass(frozen=True)
class BinaryExpression(Expression):
    operator: str
    left: Expression
    right: Expression


# Boolean conditions

@dataclass(frozen=True)
class Comparison(Condition):
    operator: str
    left: Expression
    right: Expression


@dataclass(frozen=True)
class LogicalOr(Condition):
    left: Condition
    right: Condition


@dataclass(frozen=True)
class LogicalNot(Condition):
    operand: Condition
