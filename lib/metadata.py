import json
from lib.common import SchemaRef


class MetadataView(dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def from_file(path):
        with open(path, 'r') as fh:
            metadata_dict = json.load(fh)
        return MetadataView(**metadata_dict)

    @property
    def schema_ref(self) -> SchemaRef:
        return SchemaRef(self['describedBy'])
