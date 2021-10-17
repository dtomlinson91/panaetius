from __future__ import annotations

from abc import ABCMeta, abstractmethod
import logging
from logging.handlers import RotatingFileHandler
import pathlib
import sys

from panaetius import Config
from panaetius.library import set_config
from panaetius.exceptions import LoggingDirectoryDoesNotExistException


def set_logger(config_inst: Config, logging_format_inst: LoggingData) -> logging.Logger:
    logger = logging.getLogger(config_inst.header_variable)
    log_handler_sys = logging.StreamHandler(sys.stdout)

    # configure file handler
    if config_inst.logging_path is not None:
        logging_file = (
            pathlib.Path(config_inst.logging_path)
            / config_inst.header_variable
            / f"{config_inst.header_variable}.log"
        ).expanduser()

        if not logging_file.parents[0].exists():
            raise LoggingDirectoryDoesNotExistException()

        if config_inst.logging_rotate_bytes == 0:
            set_config(config_inst, "logging.rotate_bytes", 512000)
        if config_inst.logging_backup_count == 0:
            set_config(config_inst, "logging.backup_count", 3)

        log_handler_file = RotatingFileHandler(
            str(logging_file),
            "a",
            config_inst.logging_rotate_bytes,
            config_inst.logging_backup_count,
        )

        log_handler_file.setFormatter(logging.Formatter(logging_format_inst.format))
        logger.addHandler(log_handler_file)

    # configure stdout handler
    log_handler_sys.setFormatter(logging.Formatter(logging_format_inst.format))
    logger.addHandler(log_handler_sys)
    logger.setLevel(logging_format_inst.logging_level)
    return logger


class LoggingData(metaclass=ABCMeta):
    @property
    @abstractmethod
    def format(self) -> str:
        pass

    @abstractmethod
    def __init__(self, logging_level: str):
        self.logging_level = logging_level


class SimpleLogger(LoggingData):
    @property
    def format(self) -> str:
        return str(
            '{\n\t"time": "%(asctime)s",\n\t"logging_level":'
            '"%(levelname)s",\n\t"message": "%(message)s"\n}',
        )

    def __init__(self, logging_level: str = "INFO"):
        self.logging_level = logging_level


class AdvancedLogger(LoggingData):
    @property
    def format(self) -> str:
        return str(
            '{\n\t"time": "%(asctime)s",\n\t"file_name": "%(filename)s",'
            '\n\t"module": "%(module)s",\n\t"function":"%(funcName)s",\n\t'
            '"line_number": "%(lineno)s",\n\t"logging_level":'
            '"%(levelname)s",\n\t"message": "%(message)s"\n}',
        )

    def __init__(self, logging_level: str = "INFO"):
        self.logging_level = logging_level


class CustomLogger(LoggingData):
    @property
    def format(self) -> str:
        return str(self._format)

    def __init__(self, logging_format: str, logging_level: str = "INFO"):
        self.logging_level = logging_level
        self._format = logging_format
