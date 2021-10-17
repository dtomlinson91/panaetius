from __future__ import annotations

import ast
import os
import pathlib
from typing import Any

import toml

from panaetius.exceptions import KeyErrorTooDeepException


class Config:
    """docstring for Config()."""

    def __init__(self, header_variable: str, config_path: str = "") -> None:
        self.header_variable = header_variable
        self.config_path = (
            pathlib.Path(config_path)
            if config_path
            else pathlib.Path.home() / ".config"
        )
        self._missing_config = self._check_config_file_exists()

        # default logging options
        self.logging_path: str | None = None
        self.logging_rotate_bytes: int = 0
        self.logging_backup_count: int = 0

    @property
    def config(self) -> dict:
        config_file_location = self.config_path / self.header_variable / "config.toml"
        try:
            with open(config_file_location, "r", encoding="utf-8") as config_file:
                return dict(toml.load(config_file))
        except FileNotFoundError:
            return {}

    def get_value(self, key: str, default: Any) -> Any:
        env_key = f"{self.header_variable.upper()}_{key.upper().replace('.', '_')}"

        if not self._missing_config:
            # look in the config file
            return self._get_config_value(env_key, key, default)
        # no config file, look for env vars
        return self._get_env_value(env_key, default)

    def _check_config_file_exists(self) -> bool:
        config_file_location = self.config_path / self.header_variable / "config.toml"
        try:
            with open(config_file_location, "r", encoding="utf-8"):
                return False
        except FileNotFoundError:
            return True

    def _get_config_value(self, env_key: str, key: str, default: Any) -> Any:
        try:
            # look under top header
            # REVIEW: could this be auto handled for a key of arbitrary length?
            if len(key.split(".")) > 2:
                raise KeyErrorTooDeepException(
                    f"Your key of {key} can only be 2 levels deep maximum. "
                    f"You have {len(key.split('.'))}"
                )
            if len(key.split(".")) == 1:
                return self.__get_config_value_key_split_once(key)
            if len(key.split(".")) == 2:
                return self.__get_config_value_key_split_twice(key)
            raise KeyError()

        except (KeyError, TypeError):
            value = os.environ.get(env_key.replace("-", "_"))
            if value is None:
                return self.__get_config_value_missing_key_value_is_none(default)
            # if env var, coerce value if flag is set, else return a TOML string
            return self.__get_config_value_missing_key_value_is_not_none(value)

    def __get_config_value_key_split_once(self, key: str) -> Any:
        name = key.lower()
        return self.config[self.header_variable][name]

    def __get_config_value_key_split_twice(self, key: str) -> Any:
        section, name = key.lower().split(".")
        return self.config[self.header_variable][section][name]

    def __get_config_value_missing_key_value_is_none(self, default: Any) -> Any:
        return self.__load_default_value(default)

    def __get_config_value_missing_key_value_is_not_none(self, value: str) -> Any:
        return self.__load_value(value)

    def _get_env_value(self, env_key: str, default: Any) -> Any:  # noqa
        # look for an environment variable, fallback to default
        value = os.environ.get(env_key.replace("-", "_"))
        if value is None:
            return self.__load_default_value(default)
        return self.__load_value(value)

    def __load_value(self, value: str) -> Any:  # noqa
        return ast.literal_eval(value)

    def __load_default_value(self, default: Any) -> Any:  # noqa
        return default
