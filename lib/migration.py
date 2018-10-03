import json
import typing
from copy import deepcopy

from lib import transformations
from lib.common import MigrationDirection, migration_direction
from lib.metadata import MetadataView
from lib.common import Strategy, SchemaRef


class MigrationTask:

    def __init__(self, function_name, parameters):
        self._function_name = function_name
        self._function = getattr(transformations, function_name)
        self._parameters = parameters

    @staticmethod
    def from_dict(d):
        return MigrationTask(d['function'], d['parameters'])

    def apply(self, obj):
        return self._function(obj, *self._parameters)

    def __str__(self):
        return f"MigrationTask(function_name=\'{self._function_name}\', parameters={self._parameters})"


class MigrationError(Exception):
    pass


class Migration:

    def __init__(self, source_ref, destination_ref, task_groups: typing.List[typing.List[MigrationTask]]):
        self._source_ref = SchemaRef(source_ref)
        self._destination_ref = SchemaRef(destination_ref)
        self._task_groups = task_groups

    @staticmethod
    def from_file(migrations_path) -> list:
        with open(migrations_path, 'r') as fh:
            migrations = json.load(fh)
        return [Migration.from_migration_dict(m) for m in migrations]

    @staticmethod
    def from_migration_dict(migration_dict):
        return Migration(
            migration_dict['source_ref'],
            migration_dict['destination_ref'],
            [[MigrationTask.from_dict(d) for d in g['tasks']] for g in migration_dict['task_groups']]
        )

    def migrate(self, md: MetadataView, strategy: Strategy) -> MetadataView:
        checkpoint_view = deepcopy(md)
        exact = True
        for task_group in self._task_groups:
            result = deepcopy(checkpoint_view)
            try:
                for task in task_group:
                    result = task.apply(result)
            except Exception as e:
                if strategy == strategy.EXACT:
                    # fail if we can't complete all migrations
                    raise MigrationError(f"Migration task group could not be completed: {[str(t) for t in task_group]}") from e
                elif strategy == strategy.BEST_EFFORT:
                    # skip this operation group and make best effort on others
                    exact = False
                else:
                    raise NotImplementedError("Migration strategy not implemented!")
            else:
                checkpoint_view = result
        checkpoint_view['describedBy'] = self._destination_ref.url_string
        return checkpoint_view


class MigrationCatalog:

    def __init__(self, migrations):
        self._migrations = migrations

    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as fh:
            migrations = json.load(fh)
        return MigrationCatalog(migrations)

    def get_next_migration(self, direction: MigrationDirection, source_ref: SchemaRef) -> typing.Optional[Migration]:
        try:
            migration_dict = next(
                ele for ele in self._migrations if (
                    ele['source_ref'] == source_ref.url_string and
                    migration_direction(source_ref.version, SchemaRef(ele['destination_ref']).version) == direction
                )
            )
        except StopIteration:
            return None
        return Migration.from_migration_dict(migration_dict)


class MetadataMigrator:

    def __init__(self, migration_catalog: MigrationCatalog):
        self._migration_catalog = migration_catalog

    def migrate_to_version(self, metadata: MetadataView, version: str, strategy: Strategy):
        current_view = metadata
        direction = migration_direction(current_view.schema_ref.version, version)
        while direction:
            migration = self._migration_catalog.get_next_migration(direction, current_view.schema_ref)
            if not migration:
                break
            current_view = migration.migrate(current_view, strategy)
            direction = migration_direction(current_view.schema_ref.version, version)
        return current_view
