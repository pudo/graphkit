import os
import json
from jsonschema import RefResolver, RefResolutionError

BASE = 'http://www.popoloproject.com/schemas/'
SCHEMAS = os.path.join(os.path.dirname(__file__), 'schemas')


class LocalRefResolver(RefResolver):

    def get(self, uri):
        try:
            uri, model = self.resolve(uri)
            return model
        except RefResolutionError:
            return


def create_resolver():
    resolver = LocalRefResolver(BASE, BASE)
    for fn in os.listdir(SCHEMAS):
        path = os.path.join(SCHEMAS, fn)
        with open(path, 'rb') as fh:
            data = json.load(fh)
            resolver.store[data.get('id')] = data
    return resolver

resolver = create_resolver()
