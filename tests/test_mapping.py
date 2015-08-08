import os
from unittest import TestCase

from schemaprocess.mapping import mapped_csv

from .util import RefResolver, fixture_uri, fixtures_dir


class MappingTestCase(TestCase):

    def setUp(self):
        super(MappingTestCase, self).setUp()
        self.mapping, self.uri = fixture_uri('countries/mapping.json')
        self.resolver = RefResolver(self.uri, self.mapping)
        self.csvobj = open(os.path.join(fixtures_dir, 'countries',
                                        'countries.csv'), 'rb')

    def test_basic_mapping(self):
        mapped = list(mapped_csv(self.csvobj, self.mapping,
                                 resolver=self.resolver))
        assert len(mapped) == 255, len(mapped)
        row0 = mapped[0][0]
        assert isinstance(row0, dict), row0
