import os
from unittest import TestCase

from schemaprocess.mapping import mapped_csv

from .util import RefResolver, fixture_uri, fixtures_dir


class MappingTestCase(TestCase):

    def setUp(self):
        super(MappingTestCase, self).setUp()

    def test_basic_countries_mapping(self):
        mapping, uri = fixture_uri('countries/mapping.json')
        resolver = RefResolver(uri, mapping)
        csvobj = open(os.path.join(fixtures_dir, 'countries',
                                   'countries.csv'), 'rb')
        mapped = list(mapped_csv(csvobj, mapping, resolver=resolver))
        assert len(mapped) == 255, len(mapped)
        row0, err0 = mapped[0]
        assert isinstance(row0, dict), row0
        assert err0 is not None, err0

    def test_sa_term26_mapping(self):
        mapping, uri = fixture_uri('everypol/mapping.json')
        resolver = RefResolver(uri, mapping)
        csvobj = open(os.path.join(fixtures_dir, 'everypol',
                                   'term-26.csv'), 'rb')
        mapped = list(mapped_csv(csvobj, mapping, resolver=resolver))
        assert len(mapped) == 397, len(mapped)
        row0, err0 = mapped[0]
        assert isinstance(row0, dict), row0
