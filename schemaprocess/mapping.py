import unicodecsv

from schemaprocess.util import make_resolver
from schemaprocess.visitor import SchemaVisitor


class Mapper(object):

    def __init__(self, mapping, resolver, schema=None, visitor=None):
        self._mapping = mapping.copy()
        self._schema = schema or {}
        self._visitor = visitor
        self.resolver = resolver

    @property
    def mapping(self):
        if '$ref' in self._mapping:
            uri, data = self.resolver.resolve(self._mapping.pop('$ref'))
            self._mapping.update(data)
        return self._mapping

    @property
    def schema(self):
        if '$type' in self.mapping:
            self._schema['$ref'] = self.mapping.get('$type')
        return self._schema

    @property
    def visitor(self):
        if self._visitor is None:
            self._visitor = SchemaVisitor(self.schema, self.resolver)
        return self._visitor

    def apply(self, data):
        if self.visitor.is_object:
            print 'object'
        return data


def map_iter(rows, mapping, resolver=None, base_uri=None):
    resolver = make_resolver(resolver, base_uri)
    mapper = Mapper(mapping, resolver)
    for row in rows:
        data = mapper.apply(row)
        err = {}
        yield data, err


def mapped_csv(fileobj, mapping, resolver=None, base_uri=None):
    reader = unicodecsv.DictReader(fileobj)
    for (row, err) in map_iter(reader, mapping, resolver=resolver,
                               base_uri=base_uri):
        yield (row, err)
