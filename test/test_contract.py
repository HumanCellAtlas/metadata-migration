import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from lib.common import SchemaRef
from lib.contract import *
from lib.metadata import MetadataView
from lib.schema import Schema
from test import fixture_path


class TestContract(unittest.TestCase):

    schema_ref = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/6.0.0/donor_organism")
    schema = Schema.from_ref(schema_ref)
    metadata_view_6_0_0 = MetadataView.from_file(fixture_path('donor_organism_6_0_0.json'))

    def test_conforms_to_condition(self):
        test_cases = [
            (Condition('biomaterial_core.biomaterial_id', value_type='string', required=True), True),
            (Condition('biomaterial_core.biomaterial_id', value_type='string', required=False), False),
            (Condition('biomaterial_core.biomaterial_id', value_type='int', required=True), False),
            (Condition('biomaterial_core.DNE', value_type='string', required=True), False)
        ]
        for condition, expected_result in test_cases:
            with self.subTest(f"condition={condition}, expected_result={expected_result}"):
                self.assertEqual(
                    condition.validate(self.schema),
                    expected_result
                )

    def test_conforms_to_contract(self):
        test_cases = [
            (
                Contract(
                    title='schema_has_weight',
                    conditions=[
                        Condition('weight', value_type='string', required=False),
                        Condition('weight_unit.text', value_type='string', required=True)
                    ]
                ),
                True
            ),
            (
                Contract(
                    title='schema_has_mass',
                    conditions=[
                        Condition('mass', value_type='string', required=False),
                        Condition('mass_unit.text', value_type='string', required=True)
                    ]
                ),
                False
            )
        ]
        for contract, expected_result in test_cases:
            with self.subTest(f"condition={contract}, expected_result={expected_result}"):
                self.assertEqual(
                    contract.validate(self.schema),
                    expected_result
                )

    def test_metadata_view_conforms_to_contract(self):
        test_cases = [
            (
                Contract(
                    title='metadata_view_has_weight',
                    conditions=[
                        Condition(path=None, weight=lambda x: isinstance(x, str)),
                        Condition('weight_unit', text='lbs')
                    ]
                ),
                True
            ),
            (
                Contract(
                    title='metadata_view_weight_gt_200_lbs',
                    conditions=[
                        Condition(path=None, weight=lambda w: float(w) > 200.0),
                    ]
                ),
                False
            )
        ]
        for contract, expected_result in test_cases:
            with self.subTest(f"condition={contract}, expected_result={expected_result}"):
                self.assertEqual(
                    contract.validate(self.metadata_view_6_0_0),
                    expected_result
                )
