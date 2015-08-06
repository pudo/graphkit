

class SchemaVisitor(object):
    """ A schema visitor traverses a JSON schema with associated data and
    allows the user to perform any transformations on the data that they
    wish. """

    def __init__(self, schema, resolver, data=None, name=None):
        self.schema = schema
        self.resolver = resolver
        self.data = data
        self.name = name

    @property
    def types(self):
        types = self.schema.get('type', 'object')
        if not isinstance(types, list):
            types = [types]
        return types

    @property
    def is_object(self):
        return 'object' in self.types

    @property
    def is_array(self):
        return 'array' in self.types

    @property
    def is_value(self):
        return not (self.is_object or self.is_array)

    @property
    def properties(self):
        # This will have different results depending on whether data is given
        # or not, due to pattern properties.
        pass
