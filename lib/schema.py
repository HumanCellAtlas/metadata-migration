from ingest.template.schema_template import SchemaTemplate
from lib.common import SchemaRef


class Schema(dict):

    def __init__(self, schema_ref: SchemaRef, template):
        self._schema_ref = schema_ref
        super().__init__(**template[self.schema_ref.module])

    @staticmethod
    def from_ref(ref: SchemaRef):
        return Schema(ref, SchemaTemplate(list_of_schema_urls=[ref.url_string]).get_template())

    @property
    def schema_ref(self) -> SchemaRef:
        return self._schema_ref
