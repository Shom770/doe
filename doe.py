from sys import exit

import click
from pynput.keyboard import Key, Listener
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel


from lexing.lexer import Lexer


class HandleInputs:
    def __init__(self, tokens):
        self._tokens = tokens
        self.token_pos = 0
        self.pretty_printing = True

    def press(self, key):
        if key == Key.left:
            self.token_pos -= 1 if self.token_pos != 0 else 0
        elif key == Key.right:
            self.token_pos += 1 if self.token_pos != len(self._tokens) else 0
        elif key == Key.esc:
            self.pretty_printing = False

    def start_listening(self):
        with Listener(on_press=self.press, on_release=lambda key: False) as listener:
            listener.join()


@click.command()
@click.argument("file")
@click.option("-lex", default=False, help="Display the lexed output.")
def run(file, lex):
    """Runs Doe code."""
    with open(file) as file_:
        source_code = file_.read()

    if lex:
        lexer = Lexer(source_code)

        tokens = list(lexer.lex())
        _ptr = 0

        layout = Layout(name="Pretty Printer")

        layout.split_column(
            Layout(name="source_code", ratio=8),
            Layout(name="token_info", ratio=2)
        )

        keyboard_handling = HandleInputs(tokens)

        with Live(layout, screen=True):
            while keyboard_handling.pretty_printing:
                current_token = tokens[keyboard_handling.token_pos]
                start_pos, end_pos = current_token.position

                highlighted_source = (
                    f"{source_code[:start_pos]}"
                    f"[red]{source_code[start_pos:end_pos+1]}[/red]"
                    f"{source_code[end_pos+1:]}"
                )
                layout["source_code"].update(Panel(highlighted_source))
                layout["token_info"].update(Panel(str(current_token)))
                keyboard_handling.start_listening()


if __name__ == "__main__":
    run()
