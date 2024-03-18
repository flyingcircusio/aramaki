from typing import Generator

from aramaki.models.system import SystemCategory


class RequestAPI:
    def __init__(self, request):
        self.request = request

    def navigation(self) -> Generator[SystemCategory, None, None]:
        for category in self.request.dbsession.query(SystemCategory):
            if category.anchor_systems():
                yield category


def includeme(config):
    config.add_request_method(RequestAPI, "api", reify=True)
