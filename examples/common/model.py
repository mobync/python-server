import json


class SpecialDefault:
    pass


class Model:
    uuid: str

    def __init__(self, **kwargs):
        data = {}
        for field in self.__dataclass_fields__.values():
            data[field.name] = kwargs.get(field.name, field.default)

        for key, value in data.items():
            if isinstance(value, SpecialDefault):
                value = value.get(data)

            setattr(self, key, value)

    def to_dict(self):
        data = {'uuid': self.uuid}
        for field in self.__dataclass_fields__:
            data[field] = getattr(self, field)

        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        uuid = data.pop('uuid', None)
        obj = cls(**data)
        obj.uuid = uuid
        return obj
