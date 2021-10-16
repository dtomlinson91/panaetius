from __future__ import annotations

from abc import ABC, abstractmethod
import logging
import pathlib
import sys

from panaetius import Config


def set_logger(config_inst: Config, logging_format: Logger):
    logger = logging.getLogger(config_inst.header_variable)
    loghandler_sys = logging.StreamHandler(sys.stdout)

    # check if log path is set
    if config_inst.logging_path is not None:
        logging_file = pathlib.Path(config_inst.logging_path)


class Logger(ABC):
    @property
    @abstractmethod
    def format(self):
        pass


class SimpleLogger(Logger):
    @property
    def format(self):
        return (
            '{\n\t"time": "%(asctime)s",\n\t"logging_level":'
            '"%(levelname)s",\n\t"message": "%(message)s"\n}',
        )


class AdvancedLogger(Logger):
    @property
    def format(self):
        return (
            '{\n\t"time": "%(asctime)s",\n\t"file_name": "%(filename)s",'
            '\n\t"module": "%(module)s",\n\t"function":"%(funcName)s",\n\t'
            '"line_number": "%(lineno)s",\n\t"logging_level":'
            '"%(levelname)s",\n\t"message": "%(message)s"\n}',
        )


class CustomLogger(Logger):
    @property
    def format(self):
        return self._format

    def __init__(self, logging_format: str):
        self._format = logging_format
