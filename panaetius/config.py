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

    def get_value(
        self, key: str, default: str, cast: Any = None, mask: bool = False
    ) -> Any:
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
                # TODO: set a custom error and move this to the end to tell user that incorrect key was given and couldn't be found
                # try:
                #     return cast(value) if cast else value
                # except UnboundLocalError:
                #     # pass if nothing was found
                #     pass
            except KeyError:
                # key not found in config file
                pass
            except TypeError:
                # key not found in config file
                pass

            # look for an environment variable
            value = os.environ.get(env_key.replace("-", "_"), default)


if __name__ == "__main__":
    os.environ["PANAETIUS_PATH"] = "/usr/local"
    c = Config("panaetius_test")
    print(c.config)
    c.get_value("path", "some path")
    c.get_value("top", "str", list)
    c.get_value("logging.path", "str", list)
    c.get_value("nonexistent.item", "some default value")
    pass
