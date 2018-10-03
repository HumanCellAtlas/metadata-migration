# Metadata Migration

`metadata-migration` is a proof of concept library demonstrating [Human Cell Altas](https://humancellatlas.org) metadata
migration based on "exact" and "best effort" strategies. Further, it provides a [contract
programming](https://en.wikipedia.org/wiki/Design_by_contract) module that allows users to check invariant assertions
about what schemas and instances of metadata provide.

## Contents
1. [Migration](#Migration)
1. [Contracts](#Contracts)

## <a name="Migration"></a> Migration

This section introduces concepts and modules for migration.

### `class MetadataView`

A `MetadataView` blob of metadata migrated to a new schema version. It is a "view" on the unmigrated metadata because,
often, migrations cannot guarantee that the original metadata uploader would have uploaded identical metadata under the
target schema version.

### Migration Information

`metadata-migration` uses POC migration syntax to migrate metadata. A sample migration from `donor_organism` `v6.0.0` to
a hypothetical `v6.0.1` is shown below.

```json
{
  "source_ref": "https://schema.humancellatlas.org/type/biomaterial/6.0.0/donor_organism",
  "destination_ref": "https://schema.humancellatlas.org/type/biomaterial/6.0.1/donor_organism",
  "task_groups": [
    {
      "tasks": [
        {
          "function": "pounds_to_kilograms",
          "parameters": [
            "weight",
            "weight_unit.text"
          ]
        },
        {
          "function": "move",
          "parameters": [
            "weight",
            "mass"
          ]
        },
        {
          "function": "move",
          "parameters": [
            "weight_unit",
            "mass_unit"
          ]
        }
      ]
    }
  ]
}
```

`parameters` refer to keys in the metadata. Functions are implemented as simple python functions.

`task_groups` are groups of operations that need to be completed as a transaction for the change to the metadata to be
committed. This will be discussed further in the [migration strategy](#MigrationStrategy) section.

### `class MetadataMigrator`

Metadata migrator accepts a `MetadataView` and attempts to migrate it to a specified version. The migrator can _both_
upgrade and downgrade metadata. It can migrate between any two metadata versions so long as the graph of migration
information spans the two version schemas.

Below is a sample `v6.0.0` donor organism.

```python
{
  "describedBy": "https://schema.humancellatlas.org/type/biomaterial/6.0.0/donor_organism",
  "schema_type": "biomaterial",
  "biomaterial_core": {
    "biomaterial_id": "Q4_DEMO-donor_MGH30",
    "biomaterial_name": "Q4 DEMO donor MGH30",
    "ncbi_taxon_id": [
      9606
    ]
  },
  "genus_species": [
    {
      "text": "Homo sapiens"
    }
  ],
  "organism_age": "29",
  "organism_age_unit": "year",
  "height": "178",
  "height_unit": "centimeter",
  "is_living": true,
  "biological_sex": "male",
  "weight": "160",
  "weight_unit": {
    "text": "lbs"
  },
  "provenance": {
    "document_id": "dcbe0115-7871-41de-8502-b68f6ca024ab",
    "submission_date": "2018-07-22T23:38:35.835Z",
    "update_date": "2018-07-22T23:38:44.151Z"
  }
}
```

To migrate this metadata to a different version, we load migration information, select the migration and apply it.

```python
metadata_view_6_0_0 = MetadataView.from_file('./test/fixtures/donor_organism_6_0_0.json')
migration_catalog = MigrationCatalog.from_file('./test/fixtures/migrations.json')
metadata_migrator = MetadataMigrator(migration_catalog)
metadata_migrator.migrate_to_version(metadata_view_6_0_0, '6.0.1')
{
  "describedBy": "https://schema.humancellatlas.org/type/biomaterial/6.0.1/donor_organism",
  "schema_type": "biomaterial",
  "biomaterial_core": {
    "biomaterial_id": "Q4_DEMO-donor_MGH30",
    "biomaterial_name": "Q4 DEMO donor MGH30",
    "ncbi_taxon_id": [
      9606
    ]
  },
  "genus_species": [
    {
      "text": "Homo sapiens"
    }
  ],
  "organism_age": "29",
  "organism_age_unit": "year",
  "height": "178",
  "height_unit": "centimeter",
  "is_living": true,
  "biological_sex": "male",
  "mass": "72.57472",
  "mass_unit": {
    "text": "kgs"
  },
  "provenance": {
    "document_id": "dcbe0115-7871-41de-8502-b68f6ca024ab",
    "submission_date": "2018-07-22T23:38:35.835Z",
    "update_date": "2018-07-22T23:38:44.151Z"
  }
}
```

Notice that the `weight` and `weight_unit` fields have been migrated to `mass` and `mass_unit` respectively.

#### <a name="MigrationStrategy"></a> MigrationStrategy

Metadata migrator has two migration strategies shown below.

1. `MigrationStrategy.EXACT` raises and exception if any of the migration tasks fail.
1. `MigrationStrategy.BEST_EFFORT` applies task groups one at a time. If one fails, its changes are not committed to the
   migrating `MetadataView` and the subsequent task groups are attempted.

## <a name="Contracts"></a> Contracts

### `class Condition`

A condition is an element of a contract. It accepts a path of a part of the metadata and `kwargs` key value pairs that
form assertions about a `Schema` or `MetadataView`.

```python
# Condition: schema must have required string field at path biomaterial_core.biomaterial_id
# parameters: path, **kwargs
c = Condition('biomaterial_core.biomaterial_id', value_type='string', required=True)
c.validate(schema)
```

The keys of `kwargs` refer to keys in the dictionary pointed to by the path parameter (part of the `Schema` or
`MetadataView`).  If the value of a `kwargs` pair has a value type, equality is tested between that value and the value
in the dictionary. If the value of a `kwargs` is a function that returns a boolean, that function is used to test the
value in the dictionary.

```python
# Condition: submission must have been created in the last two weeks
from dateutil.parser import parse as parse_datetime
from datetime import datetime, timedelta
c = Condition(
    'provenance',
    submission_date=lambda x: parse_datetime(x) > datetime.utcnow() - timedelta(days=14)
)
c.validate(metadata_view)
```

### `class Contract`

A contract is simply a collection of conditions that can be used to make
assertions about different parts of a `Schema` or `MetadataView`.

```python
# Contract: instance of MetadataView has weight and weight_unit info in lbs
c = Contract(
    title='metadata_view_has_weight_lbs',
    conditions=[
        Condition(path=None, weight=lambda x: isinstance(x, str)),
        Condition('weight_unit', text='lbs')
    ]
)
c.validate(metadata_view)
```

This allows developers a way to easily check if a `Schema` or `MetadataView`
conforms to their expectations before processing it.
