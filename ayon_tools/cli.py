from .commands import info_tools
from .studio import Studio
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("studio", type=str, required=False)
def info(studio_name: str | None):
    info_tools.show_studio_info(studio_name)


@cli.command()
@click.argument("studio", type=str, required=True)
@click.option("-p", "--project", type=str, required=True, help="Project Name")
def apply(studio, project):
    click.echo(f"Apply settings if studio {studio} for project {project}")

    "создать, если нету аддона, применить настройки"

@cli.command()
@click.argument("studio", type=str, required=True)
def check(studio):
    click.echo(
        f'Check differences between local and remote settings for studio "{studio}"'
    )


if __name__ == "__main__":
    cli()
