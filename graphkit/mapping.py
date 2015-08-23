import logging

import unicodecsv
from jsonmapping import Mapper

from graphkit.util import read_uri

log = logging.getLogger(__name__)


def load_mapped_csv(graph, csv_uri, mapping, context_id=None):
    """ Load data from a CSV file, applying a JSON mapping and then adding
    it to the graph. """
    meta = {'source_url': csv_uri}
    reader = unicodecsv.DictReader(read_uri(csv_uri))
    ctx = graph.context(identifier=context_id, meta=meta)
    for data, err in Mapper.apply_iter(reader, mapping, graph.resolver,
                                       scope=graph.base_uri):
        if err is not None:
            log.warning("Error loading %r: %r", csv_uri, err)
        else:
            ctx.add(data['$schema'], data)
    ctx.save()
