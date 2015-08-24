import os
import sys
import logging

import click
import yaml
from jsongraph import Graph

from graphkit.util import path_to_uri, read_yaml_uri, ensure_uri
from graphkit.mapping import load_mapped_csv
from graphkit.dumps import load_dump, save_dump, save_json_dump
from graphkit.query import save_query_json
from graphkit.admin import clear_store

log = logging.getLogger(__name__)


@click.group()
@click.option('--debug/--no-debug', default=False,
              help='Show log messages.')
@click.option('--config', '-c', default=None, metavar='FILE_URI',
              help='Graph configuration file.')
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
@click.option('--input', '-i', multiple=True,
              metavar='FILE_URI', help='Graph files to be loaded.')
@click.option('--types', '-t', multiple=True,
              metavar='ALIAS', help='Schema types to be exported.')
@click.option('--output', '-o', default=None, metavar='FILE_PATH',
              help='Path to the resulting JSON file.')
@click.option('--depth', '-r', type=int, default=4,
              help='Levels of object nesting to be exported.')
@click.pass_context
def dump_json(ctx, input, types, output, depth):
    """ Generate JSON of registered schemas. """
    graph = ctx.obj['GRAPH']
    for uri in input:
        load_dump(graph, ensure_uri(uri))
    save_json_dump(graph, output, types, depth=depth)


@cli.command('merge')
@click.option('--input', '-i', multiple=True,
              metavar='FILE_URI', help='Graph files to be loaded.')
@click.option('--output', '-o', default=None, metavar='FILE_PATH',
              help='Combined graph file.')
@click.pass_context
def merge(ctx, input, output):
    """ Combine multiple graph files. """
    graph = ctx.obj['GRAPH']
    for uri in input:
        load_dump(graph, ensure_uri(uri))
    save_dump(graph, output)


@cli.command('query')
@click.option('--input', '-i', multiple=True,
              metavar='FILE_URI', help='Graph files to be loaded.')
@click.option('--output', '-o', default=None, metavar='FILE_PATH',
              help='Path to the resulting JSON file.')
@click.option('--context', '-x', default=None,
              help='Name of the graph metadata context')
@click.option('--query-file', '-f', default=None, metavar='FILE_URI',
              help='JSON/YAML file containing the query.')
@click.pass_context
def query(ctx, input, output, context, query_file):
    """ Run an MQL query and store the results. """
    graph = ctx.obj['GRAPH']
    for uri in input:
        load_dump(graph, ensure_uri(uri))

    if query_file is not None:
        query = read_yaml_uri(ensure_uri(query_file))
    else:
        query = yaml.loads(sys.stdin)
    save_query_json(graph, query, output, context_id=context)


@cli.command('clear')
@click.option('--context', '-x', default=None,
              help='Name of the graph metadata context')
@click.pass_context
def clear(ctx, context):
    """ Delete data from the store. """
    graph = ctx.obj['GRAPH']
    clear_store(graph, context_id=context)


if __name__ == '__main__':
    cli(obj={})
