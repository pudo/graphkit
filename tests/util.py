import os
import json
import urllib

from graphkit.util import read_yaml_uri

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def fixture_file(path):
    file_name = os.path.join(fixtures_dir, path)
    return open(file_name, 'rb')


def fixture_uri(path):
    base = os.path.join(fixtures_dir, path)
    base_uri = 'file://' + urllib.pathname2url(base)
    return read_yaml_uri(base_uri), base_uri
