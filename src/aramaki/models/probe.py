from typing import Union

from typing_extensions import TypeAlias

from aramaki.models.system import System

JSONValue: TypeAlias = Union[
    int, float, str, None, bool, "JSONArray", "JSONObject"
]
JSONArray: TypeAlias = list[JSONValue]
JSONObject: TypeAlias = dict[str, JSONValue]


class Probe(object):
    name: str
    system: System
    data: JSONValue

    @classmethod
    def from_dict(self, data):
        pass
