import os

from typing import Any

from flask import Flask

from .config import Config
from .routing import Routing


class FlaskApp(Flask):
    config_class = Config
    routing_class = Routing
    routing: Routing

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routing = self.get_routing()
        self.config.from_mapping(os.environ)

    def app(self, name: str) -> Any:
        return self.extensions.get(name)

    def get_routing(self) -> Routing:
        return self.routing_class()

    def include(self, module_path: str, url: str = "", ignore_name: bool = False):
        self.routing.module(module_path, url, ignore_name)

    def append(self, url: str = "", *args, **kwargs):
        self.routing.url(url, *args, **kwargs)
