import pathlib

import toml

import panaetius


def test_default_config_path_set(header):
    # act
    config = panaetius.Config(header)

    # assert
    assert str(config.config_path) == str(pathlib.Path.home() / ".config")


def test_user_config_path_set(header, datadir):
    # arrange
    config_path = str(datadir / "without_logging")

    # act
    config = panaetius.Config(header, config_path)

    # assert
    assert str(config.config_path) == config_path


def test_config_file_exists(header, datadir):
    # arrange
    config_path = str(datadir / "without_logging")

    # act
    config = panaetius.Config(header, config_path)
    config_contents = config.config

    # assert
    assert config._missing_config == False
