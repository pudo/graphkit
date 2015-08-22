from unicodecsv import DictReader, writer

from graphkit import util
from graphkit.util import GraphKitException
from graphkit.pipe.step import Step


class CSVRead(Step):
    """ Read rows of data from a CSV file. """

    YIELDS = dict

    def apply(self, records):
        file_name = self.config.get('file')
        file_url = self.make_uri(file_name)
        fh = util.as_fh(file_url)
        for row in DictReader(fh):
            yield row
        if hasattr(fh, 'close'):
            fh.close()


class CSVWrite(Step):
    """ Read rows of data from a CSV file. """

    ACCEPTS = dict

    def apply(self, records):
        file_name = self.config.get('file')
        if file_name is None:
            raise GraphKitException("No file for export specified")
        file_name = util.to_path(self.make_uri(file_name))
        with open(file_name, 'wb') as fh:
            csv, fields = None, None

            for record in records:
                if csv is None:
                    fields = record.keys()
                    csv = writer(fh)
                    csv.writerow([unicode(f) for f in fields])

                data = []
                for k in fields:
                    v = record.get(k, '')
                    if v is None:
                        v = ''
                    data.append(unicode(v))
                csv.writerow(data)
                yield record
