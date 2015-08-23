import logging

import click
from jsongraph.uri import check as check_uri

from graphkit.util import GraphKitException, path_to_uri, read_yaml_uri
from graphkit.manager import Manager


log = logging.getLogger(__name__)


def ensure_uri(path_or_uri):
    if not check_uri(path_or_uri):
        return path_to_uri(path_or_uri)
    return path_or_uri


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--config', '-c', default=None)
@click.pass_context
def cli(ctx, debug, config):
    """ JSON graph-based data processing utility. """
    ctx.obj = ctx.obj or {}
    ctx.obj['DEBUG'] = debug

    fmt = '[%(levelname)-8s] %(name)-12s: %(message)s'
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=fmt)
    logging.getLogger('requests').setLevel(logging.WARNING)

    data = None
    if config is not None:
        data = read_yaml_uri(ensure_uri(config))

    ctx.obj['MANAGER'] = Manager(data, base_uri=config)


@cli.command('load-csv')
@click.option('--mapping', '-m', required=True)
@click.option('--output', '-o', default=None)
@click.argument('csv_file', nargs=1)
@click.pass_context
def load_csv(ctx, mapping, output, csv_file):
    """ Load entities from a CSV file. """
    manager = ctx.obj['MANAGER']
    mapping = ensure_uri(mapping)
    csv_file = ensure_uri(csv_file)
    log.debug('Loading data from %r using mapping %r', csv_file, mapping)
    manager.load_mapped_csv(csv_file, read_yaml_uri(mapping))
    if output is not None:
        manager.save_dump(output)


if __name__ == '__main__':
    cli(obj={})
