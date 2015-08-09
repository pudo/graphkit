
class RefScoped(object):
    """ Objects which have a JSON schema-style scope. """

    def __init__(self, resolver, scoped, scope=None, parent=None):
        self.resolver = resolver
        self._scoped = scoped
        self._scope = scope or ''
        self.parent = parent

    @property
    def id(self):
        return self._scoped.get('id')

    @property
    def scope(self):
        if self.id:
            return self.id
        if self.parent:
            return self.parent.scope
        return self._scope
