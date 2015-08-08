import os
from unittest import TestCase

from schemaprocess.mapping import mapped_csv

from .util import resolver, fixtures_dir


class MappingTestCase(TestCase):

    def setUp(self):
        super(MappingTestCase, self).setUp()
        _, self.mapping = resolver.resolve('countries/mapping.json')
        self.csvobj = open(os.path.join(fixtures_dir, 'countries',
                                        'countries.csv'), 'rb')

    def test_index(self):
        x = list(mapped_csv(self.csvobj, self.mapping))
        print len(x)
        assert False
