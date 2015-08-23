import json

from graphkit.dumps import _fileobj


def save_query_json(graph, query, dump_file, context_id=None):
    """ Run a given query, and store the results to a JSON file. """
    subject = graph
    if context_id is not None:
        subject = graph.context(identifier=context_id)
    q = subject.query(query)
    fh = _fileobj(dump_file)
    json.dump(q.results(), fh, indent=2)
    fh.close()
