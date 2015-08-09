import urlparse
import urllib
# from rdflib import URIRef
# from rdflib.namespace import split_uri


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


# def full_uri(graph, uri):
#     try:
#         ns, name = split_uri(uri)
#         ns = ns.rstrip(':')
#         for (prefix, ref) in graph.namespaces():
#             if prefix == ns:
#                 return URIRef(ref + name)
#     except Exception, ex:
#         print ex
#         pass
#     return URIRef(uri)
