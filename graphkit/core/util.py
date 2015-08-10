
class RefScoped(object):
    """ Objects which have a JSON schema-style scope. """

    def __init__(self, resolver, scoped, scope=None, parent=None, name=None):
        self.resolver = resolver
        self._scoped = scoped
        self._scope = scope or ''
        self.name = name
        self.parent = parent

    @property
    def id(self):
        return self._scoped.get('id')

    @property
    def path(self):
        if self.id:
            return self.id
        if self.parent and self.name:
            path = self.parent.path
            sep = '/' if '#' in path else '#/'
            return '%s%s%s' % (path, sep, self.name)

    @property
    def scope(self):
        if self.id:
            return self.id
        if self.parent:
            return self.parent.scope
        return self._scope


class GraphKitException(Exception):
    """ Base class for library exceptions. """
