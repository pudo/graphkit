from nose.tools import raises
from unittest import TestCase

from graphkit import Pipeline
from graphkit.core import GraphKitException
from .util import resolver, fixture_uri, fixture_file


class PipelineTestCase(TestCase):

    def setUp(self):
        super(PipelineTestCase, self).setUp()

    def test_pipeline_empty(self):
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
