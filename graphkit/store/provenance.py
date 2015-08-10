import urllib
from datetime import datetime

from rdflib import URIRef, Literal
from rdflib.namespace import RDF

from graphkit.store.vocab import META, BNode, get_graph
from graphkit.store.util import safe_url, is_url


def get_context(source_url=None, source_title=None, source_file=None):
    """ Generate a graph with some provenance information attached to it. """
    identifier = URIRef(safe_url(source_url)) if is_url(source_url) else None
    if identifier is None:
        if source_file is not None:
            identifier = 'file://' + urllib.pathname2url(source_file)
            identifier = URIRef(identifier)
        else:
            identifier = BNode()
    ctx = get_graph(identifier=identifier)
    ctx.add((identifier, RDF.type, META.Provenance))
    if source_url:
        ctx.add((identifier, META.sourceUrl, URIRef(safe_url(source_url))))
    if source_title:
        ctx.add((identifier, META.source, Literal(source_title)))
    if source_file:
        ctx.add((identifier, META.sourceFile, Literal(source_file)))
    ctx.add((identifier, META.created, Literal(datetime.utcnow())))
    return ctx
