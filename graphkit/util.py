import os
import json
import urllib

from jsonschema import Draft4Validator, RefResolver


def make_resolver(resolver=None, base_uri=None):
    if resolver is not None:
        return resolver
    if base_uri is None:
        base_uri = 'file://' + urllib.url2pathname(os.path.dirname(__file__))
    return RefResolver(base_uri, {})


def validate_mapping(mapping):
    """ Validate a mapping configuration file against the relevant schema. """
    file_path = os.path.join(os.path.dirname(__file__),
                             'schemas', 'mapping.json')
    with open(file_path, 'rb') as fh:
        validator = Draft4Validator(json.load(fh))
        validator.validate(mapping)
    return mapping
