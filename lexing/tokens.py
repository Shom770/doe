from enum import Enum


class TokenKind(Enum):
    """The kind of token the token itself holds."""
    INTEGER = 1
    FLOAT = 2
    ADD = 3
    SUBTRACT = 4
    MULTIPLY = 5
    DIVIDE = 6
    EXP = 7
    IDENTIFIER = 8
    KEYWORD = 9


class Token:
    """A single token that represents a part of the text."""

    def __init__(self, kind: TokenKind, value: str, start: int, end: int):
        self.kind = kind
        self.value = value
        self.position = (start, end)

    def __repr__(self):
        return f"Token(kind={self.kind}, value={self.value}, start={self.position[0]}, end={self.position[1]})"

    def __str__(self):
        return f"{self.value} of kind {self.kind} at {self.position[0]}:{self.position[1]}"
