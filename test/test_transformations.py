import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from lib import transformations


class TestTransformations(unittest.TestCase):

    def test_version_compare(self):
        d = {'a': {'b': 1}}
        transformations.move(d, 'a.b', 'd.c')
        self.assertDictEqual(d, {'a': dict(), 'd': {'c': 1}})

    def test_pounds_to_kilograms(self):
        d = {'human_specific': {'weight_unit': 'lbs', 'weight': '160'}}
        transformations.pounds_to_kilograms(d, 'human_specific.weight', 'human_specific.weight_unit')
        self.assertDictEqual(d, {'human_specific': {'weight': '72.57472', 'weight_unit': 'kgs'}})


if __name__ == '__main__':
    unittest.main()
