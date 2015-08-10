import unicodecsv

from graphkit.mapping.mapper import Mapper


def csv_mapper(fileobj, mapping, resolver=None, scope=None):
    """ Given a CSV file object (fh), parse the file as a unicode CSV document,
    iterate over all rows of the data and map them to a JSON schema using the
    mapping instructions in ``mapping``. """
    reader = unicodecsv.DictReader(fileobj)
    for (row, err) in Mapper.from_iter(reader, mapping, resolver=resolver,
                                       scope=scope):
        yield (row, err)
