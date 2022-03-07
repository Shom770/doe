import click

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

        for token in lexer.lex():
            click.echo(token)


if __name__ == "__main__":
    run()
