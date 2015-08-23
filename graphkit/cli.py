import os
import logging

import click
from jsongraph import Graph
from jsongraph.uri import check as check_uri

from graphkit.util import path_to_uri, read_yaml_uri
from graphkit.mapping import load_mapped_csv
from graphkit.dumps import load_dump, save_dump, save_json_dump

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
    else:
        config = path_to_uri(os.getcwd())

    ctx.obj['GRAPH'] = Graph(config=data, base_uri=config)


@cli.command('load-csv')
@click.option('--mapping', '-m', required=True, metavar='FILE_URI',
              help='jsonmapping for CSV to JSON Schema transform.')
@click.option('--output', '-o', default=None, metavar='FILE_URI',
              help='File to store the resulting graph.')
@click.option('--context', '-x', default=None,
              help='Name of the graph metadata context')
@click.argument('csv_file', nargs=1)
@click.pass_context
def load_csv(ctx, mapping, output, context, csv_file):
    """ Load entities from a CSV file. """
    graph = ctx.obj['GRAPH']
    mapping = ensure_uri(mapping)
    csv_uri = ensure_uri(csv_file)
    log.debug('Loading data from %r', csv_uri)
    load_mapped_csv(graph, csv_uri, read_yaml_uri(mapping), context_id=context)
    if output is not None:
        save_dump(graph, output)


@cli.command('dump-json')
@click.option('--input', '-i', required=True, multiple=True,
              metavar='FILE_URI', help='Graph files to be loaded.')
@click.option('--types', '-t', multiple=True,
              metavar='ALIAS', help='Schema types to be exported.')
@click.option('--output', '-o', default=None, metavar='FILE_PATH',
              help='Path to the resulting JSON file.')
@click.option('--depth', '-r', type=int, default=4,
              help='Levels of object nesting to be exported.')
@click.pass_context
def dump_json(ctx, input, types, output, depth):
    """ Generate a JSON representation of registered schemas. """
    graph = ctx.obj['GRAPH']
    for uri in input:
        load_dump(graph, ensure_uri(uri))
    save_json_dump(graph, output, types, depth=depth)


# @cli.command('query')
# @click.option('--results', '-r', default=None)
# @click.pass_context
# def query(ctx, mapping, output, csv_file):
#     """ Run an MQL query and print the results. """
#     manager = ctx.obj['MANAGER']
#     if output is not None:
#         manager.save_dump(output)


if __name__ == '__main__':
    cli(obj={})
