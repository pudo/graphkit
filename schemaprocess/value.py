import six
from hashlib import sha1
from normality import slugify as _slugify
import typecast


def extract_value(mapping, bind, data):
    columns = mapping.get('columns', [mapping.get('column')])
    values = [data.get(c) for c in columns]

    for transform in mapping.get('transforms', []):
        values = list(TRANSFORMS[transform](mapping, bind, values))

    value = values[0] if len(values) else None
    empty = value is None or \
        (isinstance(value, six.string_types) and not len(value.strip()))

    if empty:
        value = mapping.get('default') or bind.schema.get('default')
    return empty, convert_value(bind, value)


def convert_value(bind, value):
    for type_name in ('decimal', 'integer', 'boolean', 'number'):
        if type_name in bind.types:
            try:
                return typecast.cast(type_name, value)
            except typecast.ConverterError:
                pass
    return value


def coalesce(mapping, bind, values):
    for value in values:
        if value is not None:
            return [value]


def slugify(mapping, bind, values):
    return [_slugify(v) for v in values]


def join(mapping, bind, values):
    return [''.join([six.text_type(v) for v in values])]


def str_func(name):
    def func(mapping, bind, values):
        for v in values:
            if isinstance(v, six.string_types):
                v = getattr(v, name)()
            yield v
    return func


def hash(mapping, bind, values):
    for v in values:
        if isinstance(v, six.string_types):
            v = v.encode('utf-8')
        else:
            v = six.text_type(v)
        yield sha1(v).hexdigest()


TRANSFORMS = {
    'coalesce': coalesce,
    'slugify': slugify,
    'join': join,
    'upper': str_func('upper'),
    'lower': str_func('lower'),
    'strip': str_func('strip'),
    'hash': hash
}
