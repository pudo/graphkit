import os
import json
import urllib

from jsonschema import RefResolver

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
fixtures_dir_uri = 'file://' + urllib.url2pathname(fixtures_dir)

base = os.path.join(fixtures_dir, 'test.json')
base_uri = 'file://' + urllib.url2pathname(base)

resolver = RefResolver(base_uri, base_uri)
