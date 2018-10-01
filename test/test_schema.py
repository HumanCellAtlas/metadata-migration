import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from lib.common import SchemaRef
from lib.schema import Schema


class TestSchema(unittest.TestCase):

    schema_ref = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/6.0.0/donor_organism")
    schema = Schema.from_ref(schema_ref)

    def test_schema_ref(self):
        self.assertEqual(self.schema_ref, self.schema.schema_ref)
