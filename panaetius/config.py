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
        try:
            with open(config_file_location, "r", encoding="utf-8") as config_file:
                return dict(toml.load(config_file))
        except FileNotFoundError:
            self._missing_config = True
            return {}

    # TODO: fix the return error
    def get_value(
        self, key: str, default: Any, mask: bool, coerce: bool = False
    ) -> Any:
        env_key = f"{self.header_variable.upper()}_{key.upper().replace('.', '_')}"

        if not self._missing_config:
            # look in the config file
            return self._get_config_value(env_key, key, default, mask, coerce)
        # no config file, look for env vars
        return self._get_env_value(env_key, default, coerce)

    def _get_config_value(
        self, env_key: str, key: str, default: Any, mask: bool, coerce: bool = False
    ) -> Any:
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

        except (KeyError, TypeError):
            value = os.environ.get(env_key.replace("-", "_"))
            if value is None:
                if isinstance(default, str):
                    # if default is a string, wrap TOML value in quotes
                    return toml.loads(f'value = "{default}"')["value"]
                # if default is not a string, leave TOML value as is
                # if default is a bool, convert to lower case for TOML syntax
                default = str(default).lower() if isinstance(default, bool) else default
                return (
                    toml.loads(f"value = {default}")["value"]
                    if default is not None
                    else None
                )
            # if env var, coerce value if flag is set, else return a TOML string
            return (
                toml.loads(f"value = {value}")["value"]
                if coerce
                else toml.loads(f'value = "{value}"')["value"]
            )

    def _get_env_value(  # noqa
        self, env_key: str, default: Any, coerce: bool = False
    ) -> Any:
        # look for an environment variable, fallback to default
        value = os.environ.get(env_key.replace("-", "_"))
        if value is None:
            if isinstance(default, str):
                # if default is a string, wrap TOML value in quotes
                return toml.loads(f'value = "{default}"')["value"]
            # if default is not a string, leave TOML value as is
            # if default is a bool, convert to lower case for TOML syntax
            default = str(default).lower() if isinstance(default, bool) else default
            return (
                toml.loads(f"value = {default}")["value"]
                if default is not None
                else None
            )
        return (
            toml.loads(f"value = {value}")["value"]
            if coerce
            else toml.loads(f'value = "{value}"')["value"]
        )
