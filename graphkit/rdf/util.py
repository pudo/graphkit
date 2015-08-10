import urlparse
import urllib
from StringIO import StringIO
from rdflib.plugins.serializers.n3 import N3Serializer


def safe_url(url):
    if url is not None:
        (a, b, c, d, e) = urlparse.urlsplit(url)
        d = urllib.urlencode([(k, v.encode('utf-8'))
                              for (k, v) in urlparse.parse_qsl(d)])
        return urlparse.urlunsplit((a, b, c, d, e)).strip()


def is_url(text):
    if text is None:
        return False
    text = text.lower()
    return text.startswith('http://') or text.startswith('https://') or \
        text.startswith('urn:') or text.startswith('file://')


def query_header(graph):
    """ Declare namespace bindings for SPARQL queries. """
    sio = StringIO()
    N3Serializer(graph).serialize(sio)
    return sio.getvalue()
