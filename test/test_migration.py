import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from test import *

from lib.common import MigrationDirection
from lib.migration import Strategy, MigrationError
from lib.metadata import MetadataView


class TestMigrationCatalog(unittest.TestCase):

    def test_get_next_migration(self):
        result = migration_catalog.get_next_migration(MigrationDirection.UPGRADE, schema_ref_5_1_0)
        self.assertEqual(result._source_ref, schema_ref_5_1_0)
        self.assertEqual(result._destination_ref, schema_ref_5_1_1)

        result = migration_catalog.get_next_migration(MigrationDirection.DOWNGRADE, schema_ref_5_1_1)
        self.assertEqual(result._source_ref, schema_ref_5_1_1)
        self.assertEqual(result._destination_ref, schema_ref_5_1_0)


class TestMigration(unittest.TestCase):

    metadata_view_6_0_0 = None
    metadata_view_6_0_1 = None

    def setUp(self):
        # reload fixtures each time since they are mutated in migration
        self.metadata_view_6_0_0 = MetadataView.from_file(fixture_path('donor_organism_6_0_0.json'))
        self.metadata_view_6_0_1 = MetadataView.from_file(fixture_path('donor_organism_6_0_1.json'))

    def test_migrate_exact(self):
        migration = migration_catalog.get_next_migration(MigrationDirection.UPGRADE, schema_ref_6_0_0)
        result = migration.migrate(self.metadata_view_6_0_0, Strategy.EXACT)
        self.assertDictEqual(result, self.metadata_view_6_0_1)

        migration = migration_catalog.get_next_migration(MigrationDirection.DOWNGRADE, schema_ref_6_0_1)
        result = migration.migrate(self.metadata_view_6_0_1, Strategy.EXACT)
        self.assertDictEqual(result, metadata_view_6_0_1_downgraded_to_6_0_0)

    def test_migrate_best_effort(self):
        migration = migration_catalog.get_next_migration(MigrationDirection.DOWNGRADE, schema_ref_6_0_0)
        result = migration.migrate(self.metadata_view_6_0_0, Strategy.BEST_EFFORT)
        self.assertDictEqual(result, metadata_view_6_0_0_downgraded_to_5_9_9)


class TestMetadataMigrator(unittest.TestCase):

    metadata_view_6_0_1 = None

    def setUp(self):
        # reload fixtures each time since they are mutated in migration
        self.metadata_view_6_0_1 = MetadataView.from_file(fixture_path('donor_organism_6_0_1.json'))

    def test_migrate_to_version_exact(self):
        with self.assertRaises(MigrationError):
            metadata_migrator.migrate_to_version(self.metadata_view_6_0_1, '5.9.9', Strategy.EXACT)

    def test_migrate_to_version_best_effort(self):
        result = metadata_migrator.migrate_to_version(self.metadata_view_6_0_1, '5.9.9', Strategy.BEST_EFFORT)
        self.assertDictEqual(result, metadata_view_6_0_1_downgraded_to_5_9_9)
