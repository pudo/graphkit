from pkg_resources import iter_entry_points

from graphkit.core import GraphKitException


class Step(object):
    """ A stage within a pipeline. Any processing operation in GraphKit should
    implement a sub-class of ``Step`` and implement the defined API. The stage
    will be instantiated with an appropriate configuration derived from the
    pipeline specification. """

    # Signature definition for this step. If any of these are set to
    # not none, they will be used to determine the inputs and outputs
    # for this step.
    ACCEPTS = None  # The input data type, if any.
    YIELDS = None  # Result is an iterator with items of the given type.
    RETURNS = None  # Result is a single value of the given type.

    # Available ``Steps`` are announced via entrypoints using this namespace:
    NAMESPACE = 'graphkit.steps'

    def __init__(self, pipeline, config):
        self.pipeline = pipeline
        self.config = config

    @property
    def name(self):
        return self.config.get('step')

    def process(self, record):
        """ Handle a single record accepted by the step and either yield or
        return the output. """
        raise NotImplemented()

    def generate(self):
        """ If no input is accepted, this function is called instead to create
        output: either a single return value, or an iterator of items. """
        raise NotImplemented()

    @classmethod
    def by_name(cls, name):
        """ Load a step from Python entry points, defined by ``nmae``. """
        for ep in iter_entry_points(cls.NAMESPACE):
            if ep.name == name:
                return ep.load()
        raise GraphKitException("Cannot find step: %r" % name)
