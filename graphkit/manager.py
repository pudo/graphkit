import os

from rdflib import plugin
from rdflib.store import Store
from jsongraph import Graph, sparql_store
from jsonschema import Draft4Validator, ValidationError

from graphkit.util import GraphKitException
from graphkit.util import read_yaml_uri, path_to_uri

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

    @classmethod
    def from_uri(cls, uri):
        """ Create a ``Manager`` from a URI. """
        return cls(read_yaml_uri(uri), base_uri=uri)

    def __repr__(self):
        return '<Manager(%s)>' % self.base_uri
