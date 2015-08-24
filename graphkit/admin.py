

def clear_store(graph, context_id=None):
    """ Clear the given context, or the entire store. """
    graph.clear(context=context_id)
