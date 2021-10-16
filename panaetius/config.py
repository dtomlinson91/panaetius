from __future__ import annotations
import os
import pathlib
from typing import Any

import toml


class Config:
    """docstring for Config()."""

    def __init__(self, header_variable: str, config_path: str = "") -> None:
        self.header_variable = header_variable
        self.config_path = (
            pathlib.Path(config_path)
            if config_path
            else pathlib.Path.home() / ".config"
        )
        self._missing_config = False

    @property
    def config(self) -> dict[str, Any]:
        config_file_location = self.config_path / self.header_variable / "config.toml"
        print(config_file_location)
        try:
            with open(config_file_location, "r", encoding="utf-8") as config_file:
                return dict(toml.load(config_file))
        except FileNotFoundError:
            self._missing_config = True
            return {}

    # TODO: fix the return error
    def get_value(self, key: str, default: str | None, mask: bool) -> Any:
        env_key = f"{self.header_variable.upper()}_{key.upper().replace('.', '_')}"

        # look in the config file
        if not self._missing_config:
            try:
                # look under top header
                if len(key.split(".")) == 1:
                    if mask:
                        # TODO: write mask logic here
                        pass
                    else:
                        name = key.lower()
                        value = self.config[self.header_variable][name]
                elif len(key.split(".")) == 2:
                    if mask:
                        # TODO: write mask logic here
                        pass
                    else:
                        section, name = key.lower().split(".")
                        value = self.config[self.header_variable][section][name]
                return value
                # TODO: set a custom error and move this to the end to tell user that incorrect key was given and couldn't be found
                # try:
                #     return cast(value) if cast else value
                # except UnboundLocalError:
                #     # pass if nothing was found
                #     pass
            except (KeyError, TypeError):
                value = os.environ.get(env_key.replace("-", "_"))
                if value is None:
                    return toml.loads(default) if default is not None else None
                return toml.loads(value)
        else:
            # look for an environment variable, fallback to default
            value = os.environ.get(env_key.replace("-", "_"))
            if value is None:
                return toml.loads(default) if default is not None else None
            return toml.loads(value)
        return default
