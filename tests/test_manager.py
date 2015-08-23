from nose.tools import raises
from unittest import TestCase

from graphkit import Manager

from .util import fixture_uri


class ManagerTestCase(TestCase):

    def setUp(self):
        super(ManagerTestCase, self).setUp()
        self.data, self.uri = fixture_uri('demo.yaml')

    def test_create_manager(self):
        manager = Manager(self.data, base_uri=self.uri)
        assert manager.base_uri == self.uri
        assert self.uri in repr(manager), repr(manager)

        manager2 = Manager.from_uri(self.uri)
        assert manager2.base_uri == manager.base_uri

    def test_manager_store(self):
        manager = Manager(self.data, base_uri=self.uri)
        assert manager.store is not None
        assert 'IOMemory' in repr(manager.store)

        data = self.data.copy()
        data['store'] = {
            'query': 'http://localhost:3030/gk-test/query',
            'update': 'http://localhost:3030/gk-test/update'
        }
        manager2 = Manager(data, self.uri)
        assert manager2.store is not None, manager2.store
        assert 'SPARQLUpdateStore' in repr(manager2.store), manager2.store

    def test_basic_graph(self):
        manager = Manager(self.data, base_uri=self.uri)
        g = manager.graph
        assert str(g) == self.uri, (g, self.uri)
        assert g.get_uri('persons') == 'http://foo.bar/#person', \
            g.get_uri('persons')
