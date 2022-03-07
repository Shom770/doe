from enum import Enum


class TokenKind(Enum):
    """The kind of token the token itself holds."""
    INTEGER = 1
    FLOAT = 2
    PLUS = 3
    MINUS = 4
    MULTIPLY = 5
    DIVIDE = 6
    CARAT = 7
    IDENTIFIER = 8
    KEYWORD = 9
    NEWLINE = 10
    LPAREN = 11
    RPAREN = 12
    LBRACE = 13
    RBRACE = 14
    EQUAL = 15
    EQUALEQUAL = 16
    NOTEQUAL = 17
    LESS = 18
    LESSEQUAL = 19
    GREATER = 20
    GREATEREQUAL = 21
    EXCLAMATION = 22
    EXP = 23
    DOUBLE_QUOTE = 24
    ARROW = 25


class Token:
    """A single token that represents a part of the text."""

    def __init__(self, kind: TokenKind, value: str, start: int, end: int):
        self.kind = kind
        self.value = value
        self.position = (start, end)

    def __repr__(self):
        return f"Token(kind={self.kind}, value={self.value}, start={self.position[0]}, end={self.position[1]})"

    def __str__(self):
        return f"{self.value!r} of kind {self.kind} at {self.position[0]}:{self.position[1]}"
