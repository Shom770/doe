from utils import Constraint, Has


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self._position = 0
        self.current_char = self.text[self._position]

    def __next__(self):
        self._position += 1

        if self._position >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self._position]

    def lex_region(self, constraints: Constraint):
        tok_id = ""

        while self.current_char is not None and self.current_char in constraints:
            tok_id += self.current_char
            next(self)

        print(tok_id)


lexer = Lexer("2.5324 hi")
lexer.lex_region(Has(".", occurrences=1) | Has(int))
