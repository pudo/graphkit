import os
import logging
import unicodecsv

from rdflib import plugin
from rdflib.store import Store
from jsongraph import Graph, sparql_store
from jsonschema import Draft4Validator, ValidationError
from jsonmapping import Mapper

from graphkit.util import GraphKitException
from graphkit.util import read_yaml_uri, read_uri, path_to_uri

log = logging.getLogger(__name__)
config_schema = os.path.dirname(__file__)
config_schema = os.path.join(config_schema, 'schemas', 'config.yaml')
config_schema = read_yaml_uri(path_to_uri(config_schema))
config_schema = Draft4Validator(config_schema)


class Manager(object):
    """ A graph manager uses a configuration  """

    def __init__(self, config, base_uri=None):
        self.config = config or {}
        self.base_uri = self.config.get('base_uri', base_uri)
        if self.base_uri is None:
            self.base_uri = path_to_uri(os.getcwd())
        try:
            config_schema.validate(self.config)
        except ValidationError as ve:
            raise GraphKitException(str(ve))

    @property
    def store(self):
        """ Back-end data store. """
        if not hasattr(self, '_store') or self._store is None:
            store = self.config.get('store', {})
            if store.get('query') and store.get('update'):
                self._store = sparql_store(store.get('query'),
                                           store.get('update'))
            else:
                self._store = plugin.get('IOMemory', Store)()
        return self._store

    @property
    def graph(self):
        """ JSON data processing graph. """
        if not hasattr(self, '_graph') or self._graph is None:
            self._graph = Graph(store=self.store, base_uri=self.base_uri)
            for alias, uri in self.config.get('schemas', {}).items():
                self._graph.register(alias, uri)
        return self._graph

    def load_mapped_csv(self, csv_uri, mapping):
        """ Load data from a CSV file, applying a JSON mapping and then adding
        it to the graph. """
        meta = {'source_url': csv_uri}
        reader = unicodecsv.DictReader(read_uri(csv_uri))
        ctx = self.graph.context(meta=meta)
        for data, err in Mapper.apply_iter(reader, mapping,
                                           self.graph.resolver,
                                           scope=self.base_uri):
            if err is not None:
                log.warning("Error loading %r: %r", csv_uri, err)
            else:
                ctx.add(data['$schema'], data)
        ctx.save()

    def save_dump(self, dump_file):
        """ Save a dump of the current graph to an NQuads file. """
        dump_dir = os.path.dirname(dump_file)
        try:
            os.makedirs(dump_dir)
        except:
            pass
        log.debug('Dumping to %r...', dump_file)
        self.graph.graph.serialize(dump_file, format='nquads')

    @classmethod
    def from_uri(cls, uri):
        """ Create a ``Manager`` from a URI. """
        return cls(read_yaml_uri(uri), base_uri=uri)

    def __repr__(self):
        return '<Manager(%s)>' % self.base_uri
