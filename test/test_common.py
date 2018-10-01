import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from lib.schema import SchemaRef


class TestCommon(unittest.TestCase):

    schema_ref_10_1_0 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/10.1.0/donor_organism")
    schema_ref_10_1_1 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/10.1.1/donor_organism")
    schema_ref_10_1_2 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/10.1.2/donor_organism")

    def test_version_comparisons(self):
        self.assertEqual(self.schema_ref_10_1_0 == self.schema_ref_10_1_1, False)
        self.assertEqual(self.schema_ref_10_1_1 == self.schema_ref_10_1_1, True)
        self.assertEqual(self.schema_ref_10_1_2 == self.schema_ref_10_1_1, False)

        self.assertEqual(self.schema_ref_10_1_0 != self.schema_ref_10_1_1, True)
        self.assertEqual(self.schema_ref_10_1_1 != self.schema_ref_10_1_1, False)
        self.assertEqual(self.schema_ref_10_1_2 != self.schema_ref_10_1_1, True)

        self.assertEqual(self.schema_ref_10_1_0 < self.schema_ref_10_1_1, True)
        self.assertEqual(self.schema_ref_10_1_1 < self.schema_ref_10_1_1, False)
        self.assertEqual(self.schema_ref_10_1_2 < self.schema_ref_10_1_1, False)

        self.assertEqual(self.schema_ref_10_1_0 <= self.schema_ref_10_1_1, True)
        self.assertEqual(self.schema_ref_10_1_1 <= self.schema_ref_10_1_1, True)
        self.assertEqual(self.schema_ref_10_1_2 <= self.schema_ref_10_1_1, False)

        self.assertEqual(self.schema_ref_10_1_0 >= self.schema_ref_10_1_1, False)
        self.assertEqual(self.schema_ref_10_1_1 >= self.schema_ref_10_1_1, True)
        self.assertEqual(self.schema_ref_10_1_2 >= self.schema_ref_10_1_1, True)

        self.assertEqual(self.schema_ref_10_1_0 > self.schema_ref_10_1_1, False)
        self.assertEqual(self.schema_ref_10_1_1 > self.schema_ref_10_1_1, False)
        self.assertEqual(self.schema_ref_10_1_2 > self.schema_ref_10_1_1, True)
