import os
import json
from rdflib import Graph
from unittest import TestCase

from graphkit.rdf import RDFConverter

from .util import RefResolver, fixture_file, fixtures_dir


class RDFConverterTestCase(TestCase):

    def setUp(self):
        super(RDFConverterTestCase, self).setUp()
        self.data = json.load(fixture_file('rdfconv/bt_partial.json'))

    def test_basic_import_data(self):
        ng = Graph()
        
