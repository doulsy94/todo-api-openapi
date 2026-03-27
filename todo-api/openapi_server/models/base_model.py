import datetime
import typing
from openapi_server import util

class Model:
    def __init__(self):
        self.openapi_types = {}
        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt):
        return util.deserialize_model(dikt, cls)

    def to_dict(self):
        result = {}
        for attr, _ in self.openapi_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, datetime.datetime):
                result[attr] = value.isoformat()
            elif isinstance(value, datetime.date):
                result[attr] = value.isoformat()
            else:
                result[attr] = value
        return result

    def __repr__(self):
        return str(self.to_dict())