from graphkit.core import GraphKitException
from graphkit.pipe.step import Step


class Pipeline(object):
    """ A pipeline is a series of steps for processing a graph, defined by a
    configuration. The pipeline coordinates the execution of the steps and
    provides some common functionality. """

    def __init__(self, data):
        self.data = data
        self._steps = None

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
