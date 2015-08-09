from uuid import uuid4
from rdflib import URIRef, Namespace

PRED = Namespace('p/')
ID = Namespace('id:')


def BNode():
    return URIRef(uuid4().urn)
