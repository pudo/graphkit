import os

from graphkit import uri
from graphkit.core import GraphKitException
from graphkit.pipe.step import Step


class Pipeline(object):
    """ A pipeline is a series of steps for processing a graph, defined by a
    configuration. The pipeline coordinates the execution of the steps and
    provides some common functionality. """

    def __init__(self, data, base_uri=None):
        self.data = data
        self.base_uri = data.get('base_uri', base_uri)
        if self.base_uri is None:
            self.base_uri = uri.from_path(os.getcwd())
        self._steps = None
        # TODO: resolver
        # TODO: registry

    @property
    def config(self):
        return self.data.get('config', {})

    @property
    def steps(self):
        """ The sequence of steps in this pipeline. """
        if self._steps is None:
            self._steps = []
            for config_ in self.data.get('steps', []):
                config = self.config.copy()
                config.update(config_)
                cls = Step.by_name(config.get('step'))
                step = cls(self, config)
                if not isinstance(step, Step):
                    raise GraphKitException("Not a step: %r" % cls)
                self._steps.append(step)
        return self._steps

    def execute(self):
        """ Run the pipeline. """
        chain = tuple()
        for step in self.steps:
            chain = step.apply(chain)

        if hasattr(chain, '__iter__'):
            for record in chain:
                pass

    @classmethod
    def from_file(cls, file_name):
        return cls.from_uri(uri.from_path(file_name))

    @classmethod
    def from_uri(cls, uri):
        return cls(uri.as_yaml(uri), base_uri=uri)
