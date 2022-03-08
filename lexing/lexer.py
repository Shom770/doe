from .tokens import Token, TokenKind
from .utils import BASE_CASE, Constraint, Has, In


KEYWORDS = ["for", "func"]


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

        return self._position

    def _peek_ahead(self):
        return self.text[self._position + 1] if self._position + 1 < len(self.text) else None

    def lex(self):
        op_mapping = {
            "+": TokenKind.PLUS, "-": TokenKind.MINUS, "*": TokenKind.MULTIPLY,
            "/": TokenKind.DIVIDE, "^": TokenKind.CARAT, "!": TokenKind.EXCLAMATION
        }
        misc_mapping = {
            "=": TokenKind.EQUAL, "(": TokenKind.LPAREN, ")": TokenKind.RPAREN,
            "{": TokenKind.LBRACE, "}": TokenKind.RBRACE
        }
        comp_mapping = {
            "<": TokenKind.LESS, ">": TokenKind.GREATER, "<=": TokenKind.LESSEQUAL,
            ">=": TokenKind.GREATEREQUAL, "!=": TokenKind.NOTEQUAL, "==": TokenKind.EQUALEQUAL
        }

        while self.current_char:
            match (self.current_char, self._peek_ahead()):
                case ("\n", _):
                    yield Token(TokenKind.NEWLINE, self.current_char, self._position, self._position)
                case ("*", "*"):
                    yield Token(
                        TokenKind.EXP, self.current_char + self._peek_ahead(),
                        self._position, next(self)
                    )
                case ("+" | "-" | "/" | "*" | "^" | "!" as operator, _):
                    yield Token(op_mapping[operator], self.current_char, self._position, self._position)
                case ("<" | ">" | "!" | "=" as left_comp_op, "="):
                    yield Token(
                        comp_mapping[left_comp_op + "="], self.current_char + self._peek_ahead(),
                        self._position, next(self)
                    )
                case ("<" | ">" | "!" as comp_op , _):
                    yield Token(comp_mapping[comp_op], self.current_char, self._position, self._position)
                case ("=" | "(" | ")" | "{" | "}" as misc_char, _):
                    yield Token(misc_mapping[misc_char], self.current_char, self._position, self._position)
                case ("-", ">"):
                    yield Token(TokenKind.ARROW, "->", self._position, next(self))
                case (":", ":"):
                    yield Token(TokenKind.DOUBLE_COLON, "::", self._position, next(self))
                case ("\"", _):
                    yield self._lex_region(
                        Has("\"", occurrences=2, enforce_occurrences=True) | Has(str),
                        token_kinds=TokenKind.STRING,
                        add_occurrence="\""
                    )
                case (char, _) if char.isnumeric() or char == ".":
                    yield self._lex_region(
                        Has(".", occurrences=1) | Has(int),
                        token_kinds={TokenKind.FLOAT: Has("."), TokenKind.INTEGER: BASE_CASE}
                    )
                case (char, _) if char.isalpha():
                    yield self._lex_region(
                        Has(lambda char_: char_.isalpha()),
                        token_kinds={TokenKind.KEYWORD: In(KEYWORDS), TokenKind.IDENTIFIER: BASE_CASE}
                    )

            next(self)

    def _lex_region(
        self,
        constraints: Constraint | Has,
        token_kinds: TokenKind | dict[Has | In],
        add_occurrence: str | None = None
    ):
        if isinstance(constraints, Has):
            constraints = Constraint(constraints.__dict__)

        if add_occurrence:
            constraints.existing_occurrences[add_occurrence] += 1

        token_value = self.current_char
        start_position = self._position

        while self.current_char:
            next(self)
            if self.current_char not in constraints:
                self._position -= 1
                self.current_char = self.text[self._position]
                break
            if not self.current_char:
                break
            token_value += self.current_char

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
