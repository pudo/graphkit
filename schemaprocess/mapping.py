import unicodecsv

from schemaprocess.util import make_resolver
from schemaprocess.visitor import SchemaVisitor


class MappingVisitor(SchemaVisitor):

    @classmethod
    def from_mapping(cls, mapping, resolver):
        pass


def map_iter(rows, mapping, resolver=None, base_uri=None):
    resolver = make_resolver(resolver, base_uri)
    for row in rows:
        # print row
        err = {}
        yield row, err


def mapped_csv(fileobj, mapping, resolver=None, base_uri=None):
    reader = unicodecsv.DictReader(fileobj)
    for (row, err) in map_iter(reader, mapping, resolver=resolver, base_uri=base_uri):
        yield (row, err)
