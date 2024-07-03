import logging
import os

import click


@click.group()
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode")
@click.option("--stage", is_flag=True, default=False, help="Enable stage mode")
@click.pass_context
def cli(ctx, debug, stage):
    ctx.ensure_object(dict)
    if debug:
        os.environ["DEBUG"] = "1"
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode ON")


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
@click.pass_context
def apply(ctx, studio, project):
    """
    ayon_tools [options] apply <studio> [options]
    ayon_tools --stage apply studio_name -p project1 --project project2
    """
    from .commands import apply

    click.echo(f"Apply settings if studio {studio} for projects: {','.join(project)}")
    apply.run(studio, projects=project, **ctx.parent.params)


@cli.command()
@click.argument("studio", type=str, required=False)
@click.pass_context
def info(ctx, studio: str or None):
    # from .commands import info

    # debug = ctx.parent.params.get("debug")
    # stage = ctx.parent.params.get("stage")
    print(ctx.parent.params)
    # info.run(studio_name, stage=stage)


@cli.command()
@click.argument("studio", type=str, required=True)
def check(studio):
    click.echo(
        f'Check differences between local and remote settings for studio "{studio}"'
    )


if __name__ == "__main__":
    cli()
