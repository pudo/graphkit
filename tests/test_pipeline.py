from nose.tools import raises
from unittest import TestCase
from tempfile import NamedTemporaryFile

from graphkit import Pipeline
from graphkit.util import GraphKitException

from .util import resolver, fixture_uri


class PipelineTestCase(TestCase):

    def setUp(self):
        super(PipelineTestCase, self).setUp()
        _, self.uri = fixture_uri('test.json')

    def test_empty(self):
        pipeline = Pipeline({})
        assert len(pipeline.steps) == 0, pipeline.steps

    @raises(GraphKitException)
    def test_invalid_step(self):
        pipeline = Pipeline({
            'steps': [
                {'step': 'foo'}
            ]
        })
        assert not pipeline.steps

    def test_one_step(self):
        pipeline = Pipeline({
            'steps': [
                {
                    'step': 'csv:read',
                    'file': 'countries/countries.csv'
                }
            ]
        }, base_uri=self.uri)
        assert len(pipeline.steps) == 1
        pipeline.execute()

    def test_basic_pipe(self):
        out = NamedTemporaryFile()
        pipeline = Pipeline({
            'steps': [
                {
                    'step': 'csv:read',
                    'file': 'countries/countries.csv'
                },
                {
                    'step': 'csv:write',
                    'file': out.name
                }
            ]
        }, base_uri=self.uri)
        assert len(pipeline.steps) == 2
        pipeline.execute()
        out.seek(0)
        content = out.read()
        assert 'Abkhazia' in content, (out.name, content)
