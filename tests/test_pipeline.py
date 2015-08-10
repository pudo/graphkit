from unittest import TestCase

from graphkit import Pipeline
from .util import resolver, fixture_uri, fixture_file


class PipelineTestCase(TestCase):

    def setUp(self):
        super(PipelineTestCase, self).setUp()

    def test_pipeline_empty(self):
        pipeline = Pipeline({})
        assert len(pipeline.steps) == 0, pipeline.steps
