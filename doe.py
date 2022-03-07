import click
from rich.panel import Panel
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget

from lexing.lexer import Lexer


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

        class TokenDisplay(Widget):
            def render(self) -> Panel:
                token = tokens[PrettyLexer.token_pos]
                highlighted_source = (
                    "[white]"
                    f"{source_code[:token.position[0]]}[red]"
                    f"{source_code[token.position[0]:token.position[1] + 1]}[/red]{source_code[token.position[1] + 1:]}"
                    "[/white]"
                )
                return Panel(highlighted_source)

        class PrettyLexer(App):
            token_pos = Reactive(0)

            async def on_mount(self) -> None:
                await self.view.dock(TokenDisplay(), edge="top")

            def on_key(self, event):
                if event.key == "left":
                    self.token_pos -= 1 if self.token_pos != 0 else 0
                elif event.key == "right":
                    self.token_pos += 1 if self.token_pos != len(source_code) - 1 else 0

        PrettyLexer.run(log="textual.log")


if __name__ == "__main__":
    run()
