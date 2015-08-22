import os
import yaml
import urllib
import urlparse
import requests


class GraphKitException(Exception):
    """ Base class for library exceptions. """


def from_path(path):
    """ Given a file path, make a URI from it. """
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return 'file://' + urllib.pathname2url(path)


def to_path(uri):
    if uri.startswith('file://'):
        uri = uri.replace('file://', '')
    return uri


def as_fh(uri):
    """ Get a fileobj for the given URI. """
    scheme = urlparse.urlsplit(uri).scheme.lower()
    if scheme in ['http', 'https']:
        return requests.get(uri)
    return urllib.urlopen(uri)


def as_yaml(uri):
    """ Decode the given URI as YAML (or JSON). """
    return yaml.load(as_fh(uri))
