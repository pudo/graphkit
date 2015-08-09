import json
from rdflib import Graph
from unittest import TestCase

from graphkit.rdf import RDFConverter

from .util import resolver, fixture_file
from .util import PERSON_URI, ORG_URI


class RDFConverterTestCase(TestCase):

    def setUp(self):
        super(RDFConverterTestCase, self).setUp()
        self.data = json.load(fixture_file('rdfconv/bt_partial.json'))
        _, self.person_schema = resolver.resolve(PERSON_URI)
        _, self.org_schema = resolver.resolve(ORG_URI)

    def test_basic_import_data(self):
        ng = Graph()
        for org in self.data['organizations']:
            uri = RDFConverter.import_data(resolver, ng, org, self.org_schema)
            assert uri is not None

        for person in self.data['persons']:
            uri = RDFConverter.import_data(resolver, ng, person,
                                           self.person_schema)
            assert uri is not None
            obj = RDFConverter.load_uri(resolver, ng, uri, depth=3)
            assert obj['name'] == person['name']

        assert len(list(ng.triples((None, None, None)))) > 0
