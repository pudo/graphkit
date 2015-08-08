import unicodecsv
from jsonschema import Draft4Validator, ValidationError

from schemaprocess.util import make_resolver
from schemaprocess.value import extract_value
from schemaprocess.visitor import SchemaVisitor


class Mapper(object):

    def __init__(self, mapping, resolver, schema=None, bind=None, name=None):
        self._mapping = mapping.copy()
        self._schema = schema or {}
        self._bind = bind
        self._validator = None
        self.resolver = resolver
        self.name = name

    @property
    def mapping(self):
        if '$ref' in self._mapping:
            uri, data = self.resolver.resolve(self._mapping.pop('$ref'))
            self._mapping.update(data)
        return self._mapping

    @property
    def optional(self):
        return self.mapping.get('optional', False)

    @property
    def validator(self):
        if self._validator is None:
            self._validator = Draft4Validator(self.bind.schema,
                                              resolver=self.resolver)
        return self._validator

    @property
    def bind(self):
        if self._bind is None:
            if '$type' in self.mapping:
                self._schema['$ref'] = self.mapping.get('$type')
            self._bind = SchemaVisitor(self._schema, self.resolver)
        return self._bind

    @property
    def mappings(self):
        if not self.bind.is_object:
            return
        for name, mappings in self.mapping.get('mapping', {}).items():
            if hasattr(mappings, 'items'):
                mappings = [mappings]
            for mapping in mappings:
                for prop in self.bind.properties:
                    if prop.match(name):
                        yield Mapper(mapping, self.resolver,
                                     schema=prop.schema, bind=prop,
                                     name=name)

    def apply(self, data):
        if self.bind.is_object:
            obj, obj_empty = {}, True
            for mapping in self.mappings:
                empty, value = mapping.apply(data)
                if empty and mapping.optional:
                    continue
                obj_empty = False if not empty else obj_empty

                if mapping.name in obj and mapping.bind.is_array:
                    obj[mapping.name].extend(value)
                else:
                    obj[mapping.name] = value
            return obj_empty, obj

        elif self.bind.is_array:
            for item in self.bind.items:
                bind = Mapper(self.mapping, self.resolver,
                              schema=item.schema, bind=item,
                              name=self.name)
                empty, value = bind.apply(data)
                return empty, [value]

        elif self.bind.is_value:
            return extract_value(self.mapping, self.bind, data)


def map_iter(rows, mapping, resolver=None, base_uri=None):
    resolver = make_resolver(resolver, base_uri)
    mapper = Mapper(mapping, resolver)
    for row in rows:
        err = None
        _, data = mapper.apply(row)
        try:
            mapper.validator.validate(data)
        except ValidationError, ve:
            err = ve
        yield data, err


def mapped_csv(fileobj, mapping, resolver=None, base_uri=None):
    reader = unicodecsv.DictReader(fileobj)
    for (row, err) in map_iter(reader, mapping, resolver=resolver,
                               base_uri=base_uri):
        yield (row, err)
