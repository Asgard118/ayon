import logging
import os
import click


@click.group()
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable debug mode")
@click.option("-s", "--stage", is_flag=True, default=False, help="Enable stage mode")
@click.option("-f", "--fake", is_flag=True, default=False, help="Fake apply changes")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Fake apply changes")
@click.option(
    "--skip_update",
    is_flag=True,
    default=False,
    help="Do not update config repository if exists",
)
@click.option(
    "--read_current_files",
    is_flag=True,
    default=False,
    help="Read raw files from repository",
)
@click.pass_context
def cli(ctx, debug, stage, fake, skip_update, read_current_files, verbose):
    ctx.ensure_object(dict)
    if debug:
        os.environ["DEBUG"] = "1"
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode ON")

    if skip_update:
        from .repository import repo

        logging.info("Skip update config repository")
        repo.skip_update = skip_update
    if read_current_files:
        from .repository import repo

        logging.info("Read repository data from current files")
        repo.read_from_current_files = read_current_files


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
@click.option(
    "-o",
    "--operations",
    type=click.Choice(["anatomy", "attrs", "settings", "bundle"]),
    required=False,
    multiple=True,
    default=[],
)
@click.pass_context
def apply(ctx, studio, project, operations):
    """
    ayon_tools [options] apply <studio> [options]
    ayon_tools --stage apply studio_name -p project1 --project project2
    """
    from .commands import apply

    apply.run(studio, projects=project, operations=operations, **ctx.parent.params)


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
