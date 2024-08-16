import logging
import os
import sys
import tempfile

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
    from .commands import backup_restore

    backup_path = backup_restore.dump(studio, tempfile.mktemp(suffix=".json"))
    try:
        apply.run(studio, projects=project, operations=operations, **ctx.parent.params)
    except Exception as e:
        logging.error(str(e))
        backup_restore.restore(studio, backup_path)


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


@cli.command()
@click.argument("studio", type=str, required=True)
@click.option("-p", "--path", type=str, default=None, help="Path to backup")
@click.pass_context
def dump(ctx, studio, path):
    from .commands import backup_restore

    try:
        backup_restore.dump(studio, path, **ctx.parent.params)
        print(f"save backup in: {path}")
    except Exception:
        logging.exception("Bump Failed")
        sys.exit(1)


@cli.command()
@click.argument("studio", type=str, required=True)
@click.argument("backup_path", type=str, required=True)
@click.pass_context
def restore(ctx, studio, backup_path):
    from .commands import backup_restore

    try:
        backup_restore.restore(studio, backup_path, **ctx.parent.params)
    except Exception:
        logging.exception("Restore Failed")
        sys.exit(1)


if __name__ == "__main__":
    cli()
