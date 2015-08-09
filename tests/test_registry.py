from unittest import TestCase

from graphkit.core import SchemaRegistry

from .util import RefResolver, fixture_uri

PERSON_URI = 'http://www.popoloproject.com/schemas/person.json#'
ORG_URI = 'http://www.popoloproject.com/schemas/organization.json#'
MEM_URI = 'http://www.popoloproject.com/schemas/membership.json#'


class RegistryTestCase(TestCase):

    def setUp(self):
        super(RegistryTestCase, self).setUp()
        mapping, uri = fixture_uri('countries/mapping.json')
        self.resolver = RefResolver(uri, mapping)
        self.reg = SchemaRegistry(self.resolver)
        self.reg.register('person', PERSON_URI)
        self.reg.register('organization', ORG_URI)

    def test_register(self):
        assert self.reg.resolver == self.resolver, self.reg
        assert 'membership' not in self.reg.aliases
        self.reg.register('membership', MEM_URI)
        assert 'membership' in self.reg.aliases

    def test_get_uri(self):
        assert self.reg.resolver == self.resolver, self.reg
        assert 'person' in self.reg.aliases
        assert self.reg.get_uri('person') == PERSON_URI, \
            self.reg.get_uri('person')

    def test_get_schema(self):
        schema1 = self.reg.get_schema('person')
        schema2 = self.reg.get_schema(PERSON_URI)
        assert schema1 == schema2
        assert 'id' in schema1
        assert schema1['id'] == PERSON_URI
