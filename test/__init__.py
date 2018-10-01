import os
import sys

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from lib.common import SchemaRef
from lib.migration import MigrationCatalog, MetadataMigrator
from lib.metadata import MetadataView


def fixture_path(fixture_file):
    return pkg_root + '/test/fixtures/' + fixture_file


migration_catalog = MigrationCatalog.from_file(fixture_path('migrations.json'))
metadata_migrator = MetadataMigrator(migration_catalog)
schema_ref_5_1_0 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/5.1.0/donor_organism")
schema_ref_5_1_1 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/5.1.1/donor_organism")
schema_ref_5_9_9 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/5.9.9/donor_organism")
schema_ref_6_0_0 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/6.0.0/donor_organism")
schema_ref_6_0_1 = SchemaRef("https://schema.humancellatlas.org/type/biomaterial/6.0.1/donor_organism")

metadata_view_6_0_0_downgraded_to_5_9_9 = MetadataView.from_file(fixture_path('donor_organism_6_0_0_downgraded_to_5_9_9.json'))
metadata_view_6_0_1_downgraded_to_5_9_9 = MetadataView.from_file(fixture_path('donor_organism_6_0_1_downgraded_to_5_9_9.json'))
metadata_view_6_0_1_downgraded_to_6_0_0 = MetadataView.from_file(fixture_path('donor_organism_6_0_1_downgraded_to_6_0_0.json'))
