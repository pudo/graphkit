import os
import json
import urllib

from jsonschema import RefResolver  # noqa

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def fixture_uri(path):
    base = os.path.join(fixtures_dir, path)
    base_uri = 'file://' + urllib.url2pathname(base)
    with open(base, 'rb') as fh:
        return json.load(fh), base_uri
