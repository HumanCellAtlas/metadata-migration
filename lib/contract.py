import typing


class Condition:

    def __init__(self, path, **kwargs):
        self._path = path
        self._checks = kwargs

    @property
    def path(self):
        return self._path

    @property
    def checks(self) -> dict:
        return self._checks

    def _get(self, obj):
        result = obj
        if self.path:
            path_parts = self.path.split('.')
            for part in path_parts:
                result = result[part]
                if not result:
                    break
        return result

    def validate(self, obj: dict) -> bool:
        try:
            parent = self._get(obj)
        except KeyError:
            return False
        result = True
        for key, check in self.checks.items():
            if callable(check):
                tmp = check(parent[key])
                if not isinstance(tmp, bool):
                    raise Exception('Contract lambdas must evaluate to a bool!')
                result &= tmp
            else:
                result &= parent[key] == check
        return result


class Contract:

    def __init__(self, title: str, conditions: typing.List[Condition]):
        self.title = title
        self.conditions = conditions

    def validate(self, obj: dict) -> bool:
        for condition in self.conditions:
            if not condition.validate(obj):
                return False
        return True
