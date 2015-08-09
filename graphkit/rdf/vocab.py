from uuid import uuid4
from rdflib import Literal, URIRef, Namespace

POPOLO = Namespace('urn:popolo:')
ID = Namespace('id:')
BNODE = Namespace('b:')

Person = URIRef('http://www.popoloproject.com/schemas/person.json#')
Organization = URIRef('http://www.popoloproject.com/schemas/organization.json#')
Membership = URIRef('http://www.popoloproject.com/schemas/membership.json#')


def bind(graph):
    graph.bind('p', POPOLO)


def node():
    return BNODE[uuid4().hex[:20]]
