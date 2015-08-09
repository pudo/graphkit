import os
import urllib

from jsonschema import RefResolver


def make_resolver(resolver=None, base_uri=None):
    if resolver is not None:
        return resolver
    if base_uri is None:
        base_uri = 'file://' + urllib.url2pathname(os.path.dirname(__file__))
    return RefResolver(base_uri, {})
