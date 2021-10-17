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

        # default logging options
        self.logging_path: str | None = None
        self.logging_rotate_bytes: int = 0
        self.logging_backup_count: int = 0

    @property
    def config(self) -> dict[str, Any]:
        config_file_location = self.config_path / self.header_variable / "config.toml"
        try:
            with open(config_file_location, "r", encoding="utf-8") as config_file:
                return dict(toml.load(config_file))
        except FileNotFoundError:
            self._missing_config = True
            return {}

    def get_value(self, key: str, default: Any, coerce: bool = False) -> Any:
        env_key = f"{self.header_variable.upper()}_{key.upper().replace('.', '_')}"

        if not self._missing_config:
            # look in the config file
            return self._get_config_value(env_key, key, default, coerce)
        # no config file, look for env vars
        return self._get_env_value(env_key, default, coerce)

    def _get_config_value(
        self, env_key: str, key: str, default: Any, coerce: bool = False
    ) -> Any:
        try:
            # look under top header
            # REVIEW: could this be auto handled for a key of arbitrary length?
            if len(key.split(".")) == 1:
                return self.__get_config_value_key_split_once(key)
            if len(key.split(".")) == 2:
                return self.__get_config_value_key_split_twice(key)
            raise KeyError

        except (KeyError, TypeError):
            value = os.environ.get(env_key.replace("-", "_"))
            if value is None:
                return self.__get_config_value_missing_key_value_is_none(default)
            # if env var, coerce value if flag is set, else return a TOML string
            return self.__get_config_value_missing_key_value_is_not_none(value, coerce)

    def __get_config_value_key_split_once(self, key: str) -> Any:
        name = key.lower()
        return self.config[self.header_variable][name]

    def __get_config_value_key_split_twice(self, key: str) -> Any:
        section, name = key.lower().split(".")
        return self.config[self.header_variable][section][name]

    def __get_config_value_missing_key_value_is_none(self, default: Any) -> Any:
        return self.__load_default_value(default)

    def __get_config_value_missing_key_value_is_not_none(
        self, value: str, coerce: bool
    ) -> Any:
        return self.__load_value(value, coerce)

    def _get_env_value(  # noqa
        self, env_key: str, default: Any, coerce: bool = False
    ) -> Any:
        # look for an environment variable, fallback to default
        value = os.environ.get(env_key.replace("-", "_"))
        if value is None:
            return self.__load_default_value(default)
        return self.__load_value(value, coerce)

    def __load_value(self, value: str, coerce: bool) -> Any:  # noqa
        value = str(value).lower() if isinstance(value, bool) else value
        return (
            toml.loads(f"value = {value}")["value"]
            if coerce
            else toml.loads(f'value = "{value}"')["value"]
        )

    def __load_default_value(self, default: Any) -> Any:  # noqa
        if isinstance(default, str):
            return toml.loads(f'value = "{default}"')["value"]
        # if default is bool convert to lower case toml syntax
        default = str(default).lower() if isinstance(default, bool) else default
        return (
            toml.loads(f"value = {default}")["value"] if default is not None else None
        )
