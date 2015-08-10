import unicodecsv

from graphkit import uri
from graphkit.pipe.step import Step


class ReadCSV(Step):
    """ Read rows of data from a CSV file. """

    YIELDS = dict

    def generate(self):
        file_name = self.config.get('file')
        file_url = self.make_uri(file_name)
        with uri.as_fh(file_url):
            reader = unicodecsv.DictReader()
            for row in reader:
                yield row
