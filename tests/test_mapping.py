import os
from unittest import TestCase

from graphkit.mapping import csv_mapper

from .util import RefResolver, fixture_uri, fixture_file


class MappingTestCase(TestCase):

    def setUp(self):
        super(MappingTestCase, self).setUp()

    def test_basic_countries_mapping(self):
        mapping, uri = fixture_uri('countries/mapping.json')
        resolver = RefResolver(uri, mapping)
        csvobj = fixture_file('countries/countries.csv')
        mapped = list(csv_mapper(csvobj, mapping, resolver=resolver))
        assert len(mapped) == 255, len(mapped)
        row0, err0 = mapped[0]
        assert isinstance(row0, dict), row0
        assert err0 is not None, err0

    def test_sa_term26_mapping(self):
        mapping, uri = fixture_uri('everypol/mapping.json')
        resolver = RefResolver(uri, mapping)
        csvobj = fixture_file('everypol/term-26.csv')
        mapped = list(csv_mapper(csvobj, mapping, resolver=resolver))
        assert len(mapped) == 397, len(mapped)
        row0, err0 = mapped[0]
        assert isinstance(row0, dict), row0
