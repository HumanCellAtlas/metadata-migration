from enum import Enum


class MigrationDirection(Enum):
    DOWNGRADE = 1
    UPGRADE = 2


class Strategy(Enum):
    EXACT = 1
    BEST_EFFORT = 2


class SchemaRef:

    def __init__(self, url_string):
        self.url_string = url_string
        self.base_url, self.high_level_entity, self.domain_entity, self.version, self.module = url_string.rsplit('/', 4)

    def __eq__(self, other):
        return self.url_string == other.url_string

    def __ne__(self, other):
        return self.url_string != other.url_string

    def __gt__(self, other):
        self._validate(other)
        return compare_versions(other.version, self.version) > 0

    def __ge__(self, other):
        self._validate(other)
        return compare_versions(other.version, self.version) >= 0

    def __lt__(self, other):
        self._validate(other)
        return compare_versions(other.version, self.version) < 0

    def __le__(self, other):
        self._validate(other)
        return compare_versions(other.version, self.version) <= 0

    def _validate(self, other):
        if not all([
            self.base_url == other.base_url,
            self.high_level_entity == other.high_level_entity,
            self.domain_entity == other.domain_entity,
            self.module == other.module
        ]):
            raise Exception('These versions are non-comparable!')


def compare_versions(ver_a, ver_b):
    ver_a_ints = [int(i) for i in ver_a.split('.')]
    ver_b_ints = [int(i) for i in ver_b.split('.')]
    assert (len(ver_a_ints) == len(ver_b_ints))
    for a_int, b_int in zip(ver_a_ints, ver_b_ints):
        diff = b_int - a_int
        if diff != 0:
            return diff
    return 0


def migration_direction(ver_a, ver_b):
    i = compare_versions(ver_a, ver_b)
    if i < 0:
        return MigrationDirection.DOWNGRADE
    if i > 0:
        return MigrationDirection.UPGRADE
    return None
