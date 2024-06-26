import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("studio", type=str, required=False)
def info(studio_name: str or None):
    from .commands import info

    info.process(studio_name)


@cli.command()
@click.argument("studio", type=str, required=True)
@click.option(
    "-p",
    "--project",
    type=str,
    required=False,
    multiple=True,
    default=(),
    help="Project Names",
)
def apply(studio, project):
    """
    Example:
         ayon_tools apply studio_name -p project_name1 -p project_name2
    """
    from .commands import apply

    click.echo(f"Apply settings if studio {studio} for project {project}")
    apply.run(studio)


@cli.command()
@click.argument("studio", type=str, required=True)
def check(studio):
    click.echo(
        f'Check differences between local and remote settings for studio "{studio}"'
    )


if __name__ == "__main__":
    cli()
