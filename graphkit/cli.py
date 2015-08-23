import sys
import logging
import json

import click
from jsongraph.uri import check as check_uri

from graphkit.util import GraphKitException, path_to_uri, read_yaml_uri
from graphkit.util import dump_fileobj
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
@click.option('--context', '-x', default=None)
@click.argument('csv_file', nargs=1)
@click.pass_context
def load_csv(ctx, mapping, output, context, csv_file):
    """ Load entities from a CSV file. """
    manager = ctx.obj['MANAGER']
    mapping = ensure_uri(mapping)
    csv_file = ensure_uri(csv_file)
    log.debug('Loading data from %r using mapping %r', csv_file, mapping)
    manager.load_mapped_csv(csv_file, read_yaml_uri(mapping),
                            context=context)
    if output is not None:
        manager.save_dump(output)


@cli.command('to-json')
@click.option('--input', '-i', required=True, multiple=True)
@click.option('--output', '-o', default=None)
@click.option('--depth', '-r', type=int, default=3)
@click.pass_context
def to_json(ctx, input, output, depth):
    """ Generate a JSON representation of all registered schemas. """
    manager = ctx.obj['MANAGER']
    for uri in input:
        manager.load_dump(ensure_uri(uri))

    log.debug('Storing JSON dump to %r', output or 'stdout')
    if output is not None:
        fh = dump_fileobj(output)
    else:
        fh = sys.stdout

    data = {}
    for name in manager.graph.aliases:
        objects = [o for o in manager.graph.all(name, depth=depth)]
        data[name] = objects
    json.dump(data, fh, indent=2)
    fh.close()


@cli.command('query')
@click.option('--results', '-r', default=None)
@click.pass_context
def query(ctx, mapping, output, csv_file):
    """ Run an MQL query and print the results. """
    manager = ctx.obj['MANAGER']
    if output is not None:
        manager.save_dump(output)



if __name__ == '__main__':
    cli(obj={})
