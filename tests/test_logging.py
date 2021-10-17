import logging
from uuid import uuid4

import pytest

from panaetius import set_logger, SimpleLogger, Config, set_config
from panaetius.exceptions import LoggingDirectoryDoesNotExistException


def test_logging_directory_does_not_exist(header, shared_datadir):
    # arrange
    config = Config(header)
    logging_path = str(shared_datadir / str(uuid4()))
    set_config(config, "logging.path", default=str(logging_path))

    # act
    with pytest.raises(LoggingDirectoryDoesNotExistException) as logging_exception:
        _ = set_logger(config, SimpleLogger())

    # assert
    assert str(logging_exception.value) == ""


def test_logging_directory_does_exist(header, shared_datadir):
    # arrange
    config = Config(header)
    logging_path = str(shared_datadir / "without_logging")
    set_config(config, "logging.path", default=str(logging_path))

    # act
    logger = set_logger(config, SimpleLogger())

    # assert
    assert isinstance(logger, logging.Logger)
