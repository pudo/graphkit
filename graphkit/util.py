import os
import yaml
import click
import logging
import urllib
import urlparse
import requests

from jsongraph.uri import check as check_uri

log = logging.getLogger()


class GraphKitException(click.ClickException):
    """ Base class for library exceptions. """

    def show(self):
        log.error(self)

    exit_code = -1


def ensure_uri(path_or_uri):
    """ Check if the given string is a URI, otherwise make a file URI. """
    if not check_uri(path_or_uri):
        return path_to_uri(path_or_uri)
    return path_or_uri


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
    try:
        scheme = urlparse.urlsplit(uri).scheme.lower()
        if scheme in ['http', 'https']:
            return requests.get(uri)
        return urllib.urlopen(uri)
    except IOError as ioe:
        raise GraphKitException(str(ioe))


def read_yaml_uri(uri):
    """ Decode the given URI as YAML (or JSON). """
    return yaml.load(read_uri(uri))


def dump_fileobj(file_path):
    dump_dir = os.path.dirname(file_path)
    try:
        os.makedirs(dump_dir)
    except:
        pass
    return open(file_path, 'wb')
