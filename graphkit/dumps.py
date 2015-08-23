import sys
import json
import logging

from graphkit.util import read_uri, dump_fileobj
from graphkit.util import GraphKitException

log = logging.getLogger(__name__)


def _fileobj(dump_file):
    if dump_file is None:
        return sys.stdout
    return dump_fileobj(dump_file)


def save_dump(graph, dump_file):
    """ Save a dump of the current graph to an NQuads file. """
    log.debug('Dumping to %r...', dump_file or 'stdout')
    fh = _fileobj(dump_file)
    graph.graph.serialize(fh, format='nquads')
    fh.close()


def load_dump(graph, dump_file):
    """ Load an NQuads file into the current graph. """
    log.debug('Loading from %r...', dump_file)
    fh = read_uri(dump_file)
    graph.graph.parse(fh, format='nquads')
    fh.close()


def save_json_dump(graph, dump_file, types=[], depth=4):
    """ Generate a nested JSON dump of a set of objects. """
    log.debug('Storing JSON dump to %r...', dump_file or 'stdout')
    if len(types):
        for alias in types:
            if alias not in graph.aliases:
                raise GraphKitException('No such type alias: %r' % alias)
    else:
        types = graph.aliases.keys()
    data = {}
    for name in types:
        objects = [o for o in graph.all(name, depth=depth)]
        data[name] = objects

    fh = _fileobj(dump_file)
    json.dump(data, fh, indent=2)
    fh.close()
