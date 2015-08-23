import os
import yaml
import urllib
import urlparse
import requests


class GraphKitException(Exception):
    """ Base class for library exceptions. """


def path_to_uri(path):
    """ Given a file path, make a URI from it. """
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return 'file://' + urllib.pathname2url(path)


def uri_to_path(uri):
    if uri.startswith('file://'):
        return uri.replace('file://', '')


def read_uri(uri):
    """ Get a fileobj for the given URI. """
    scheme = urlparse.urlsplit(uri).scheme.lower()
    if scheme in ['http', 'https']:
        return requests.get(uri)
    return urllib.urlopen(uri)


def read_yaml_uri(uri):
    """ Decode the given URI as YAML (or JSON). """
    return yaml.load(read_uri(uri))
