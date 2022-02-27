from tokens import Token, TokenKind
from utils import BASE_CASE, Constraint, Has, In


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self._position = 0
        self.current_char = self.text[self._position]

    def __next__(self):
        self._position += 1

        if self._position >= len(self.text):
            self.current_char = None
            self._position = len(self.text) - 1
        else:
            self.current_char = self.text[self._position]

    def lex_region(self, constraints: Constraint, token_kinds: TokenKind | dict[Has | In]):
        token_value = ""
        start_position = self._position

        while self.current_char is not None and self.current_char in constraints:
            token_value += self.current_char
            next(self)

        end_position = self._position

        if isinstance(token_kinds, TokenKind):
            return Token(kind=token_kinds, value=token_value, start=start_position, end=end_position)
        else:
            for token_kind, condition in token_kinds.items():
                if isinstance(condition, Has) and condition.constraint in token_value:
                    return Token(kind=token_kind, value=token_value, start=start_position, end=end_position)
                elif isinstance(condition, In) and token_value in condition.iterable:
                    return Token(kind=token_kind, value=token_value, start=start_position, end=end_position)
                elif condition == BASE_CASE:
                    return Token(kind=token_kind, value=token_value, start=start_position, end=end_position)


lexer = Lexer("2.5324 hi")
print(lexer.lex_region(
    constraints=Has(".", occurrences=1) | Has(int),
    token_kinds={TokenKind.FLOAT: Has("."), TokenKind.INT: BASE_CASE})
)
