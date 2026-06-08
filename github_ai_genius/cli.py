import typer

app = typer.Typer()


@app.command()
def doctor():
    print('GitHub AI Genius CLI installed')


if __name__ == '__main__':
    app()
