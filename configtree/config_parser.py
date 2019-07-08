import collections
from pathlib import Path


class PropertiesParser(object):
    def __init__(self, data=None, separator="="):
        """

        :param data: a python dict
        :param separator: separator used for the properties file, usually "=" or ":"
        """
        self.data = data
        self.parsed_data = None
        self.separator = separator

    def parse_data(self):
        self.parsed_data = self._flatten(self.data)
        return self.parsed_data

    def _flatten(self, data, parent_key=''):
        properties = []
        for k, v in data.items():
            property = parent_key + "." + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                properties.extend(self._flatten(v, property).items())
            else:
                properties.append((property, v))
        return dict(properties)

    def write_file(self, path='.', filename='config'):
        path = path.rstrip('/')
        file_path = Path(path+'/'+filename)
        # check if file exists, if so stop!
        if file_path.is_file():
            return {'error': 'File already exists, will not overwrite!', 'filePath': file_path.as_posix()}

        with open(file_path, mode='w') as file:
            for k, v in self.parsed_data.items():
                file.write(str(k) + self.separator + str(v) + "\n")

        return {'success': 'file written', 'filePath': file_path.as_posix()}
