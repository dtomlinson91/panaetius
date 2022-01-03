import os
import pathlib
from uuid import uuid4

import pytest

import panaetius
from panaetius.exceptions import InvalidPythonException, KeyErrorTooDeepException

# test config paths


def test_default_config_path_set(header):
    # act
    config = panaetius.Config(header)

    # assert
    assert str(config.config_path) == str(pathlib.Path.home() / ".config")


def test_user_config_path_set(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_logging")

    # act
    config = panaetius.Config(header, config_path)

    # assert
    assert str(config.config_path) == config_path


def test_user_config_path_without_header_dir_set(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_header")

    # act
    config = panaetius.Config(header, config_path, skip_header_init=True)

    # assert
    assert str(config.config_path) == config_path


# test config files


def test_config_file_exists(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_logging")

    # act
    config = panaetius.Config(header, config_path)
    _ = config.config

    # assert
    assert config._missing_config is False


def test_config_file_without_header_dir_exists(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_header")

    # act
    config = panaetius.Config(header, config_path, skip_header_init=True)
    _ = config.config

    # assert
    assert config._missing_config is False


def test_config_file_contents_read_success(header, shared_datadir, testing_config_contents):
    # arrange
    config_path = str(shared_datadir / "without_logging")

    # act
    config = panaetius.Config(header, config_path)
    config_contents = config.config

    # assert
    assert config_contents == testing_config_contents


@pytest.mark.parametrize(
    "set_config_key,get_config_key,expected_value",
    [
        ("some_top_string", "some_top_string", "some_top_value"),
        ("second.some_second_string", "second_some_second_string", "some_second_value"),
        (
            "second.some_second_list",
            "second_some_second_list",
            ["some", "second", "value"],
        ),
        (
            "second.some_second_table",
            "second_some_second_table",
            {"first": ["some", "first", "value"]},
        ),
        (
            "second.some_second_table_bools",
            "second_some_second_table_bools",
            {"bool": [True, False]},
        ),
        ("second.third.some_third_string", "second_third_some_third_string", "some_third_value"),
    ],
)
def test_get_value_from_key(set_config_key, get_config_key, expected_value, header, shared_datadir):
    """
    Test the following:

    - keys are read from top level key
    - keys are read from two level key
    - inline arrays are read correctly
    - inline tables are read correctly
    - inline tables & arrays read bools correctly
    """
    # arrange
    config_path = str(shared_datadir / "without_logging")
    config = panaetius.Config(header, config_path)
    panaetius.set_config(config, set_config_key)

    # act
    config_value = getattr(config, get_config_key)

    # assert
    assert config_value == expected_value


def test_get_value_environment_var_override(header, shared_datadir):
    # arrange
    os.environ[f"{header.upper()}_SOME_TOP_STRING"] = "some_overridden_value"
    config_path = str(shared_datadir / "without_logging")
    config = panaetius.Config(header, config_path)
    panaetius.set_config(config, "some_top_string")

    # act
    config_value = getattr(config, "some_top_string")

    # assert
    assert config_value == "some_overridden_value"

    # cleanup
    del os.environ[f"{header.upper()}_SOME_TOP_STRING"]


def test_key_level_too_deep(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_logging")
    config = panaetius.Config(header, config_path)
    key = "a.key.too.deep"

    # act
    with pytest.raises(KeyErrorTooDeepException) as key_error_too_deep:
        panaetius.set_config(config, key)

    # assert
    assert str(key_error_too_deep.value) == f"Your key of {key} can only be 3 levels deep maximum."


def test_get_value_missing_key_from_default(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_logging")
    config = panaetius.Config(header, config_path)
    panaetius.set_config(
        config,
        "missing.key_from_default",
        default=["some", "default", "value", 1.0, True],
    )

    # act
    default_value = getattr(config, "missing_key_from_default")

    # assert
    assert default_value == ["some", "default", "value", 1.0, True]


def test_get_value_missing_key_from_env(header, shared_datadir):
    # arrange
    os.environ[f"{header.upper()}_MISSING_KEY"] = "some missing key"

    config_path = str(shared_datadir / "without_logging")
    config = panaetius.Config(header, config_path)
    panaetius.set_config(config, "missing_key")

    # act
    value_from_key = getattr(config, "missing_key")

    # assert
    assert value_from_key == "some missing key"

    # cleanup
    del os.environ[f"{header.upper()}_MISSING_KEY"]


# test env vars


def test_config_file_does_not_exist(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "nonexistent_folder")

    # act
    config = panaetius.Config(header, config_path)
    config_contents = config.config

    # assert
    assert config._missing_config is True
    assert config_contents == {}


def test_missing_config_read_from_default(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "nonexistent_folder")

    # act
    config = panaetius.Config(header, config_path)
    panaetius.set_config(config, "missing.key_read_from_default", default=True)

    # assert
    assert getattr(config, "missing_key_read_from_default") is True


@pytest.mark.parametrize(
    "env_value,expected_value",
    [
        ("a missing string", "a missing string"),
        ("1", 1),
        ("1.0", 1.0),
        ("True", True),
        (
            '["an", "array", "of", "items", 1, True]',
            ["an", "array", "of", "items", 1, True],
        ),
        (
            '{"an": "array", "of": "items", "1": True}',
            {"an": "array", "of": "items", "1": True},
        ),
    ],
)
def test_missing_config_read_from_env_var(env_value, expected_value, header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / str(uuid4()))
    os.environ[f"{header.upper()}_MISSING_KEY_READ_FROM_ENV_VAR"] = env_value

    # act
    config = panaetius.Config(header, config_path)
    panaetius.set_config(config, "missing.key_read_from_env_var")

    # assert
    assert getattr(config, "missing_key_read_from_env_var") == expected_value

    # cleanup
    del os.environ[f"{header.upper()}_MISSING_KEY_READ_FROM_ENV_VAR"]


@pytest.mark.skip(reason="No longer needed as strings are loaded without quotes")
def test_missing_config_read_from_env_var_invalid_python(header):
    # arrange
    os.environ[f"{header.upper()}_INVALID_PYTHON"] = "a string without quotes"
    config = panaetius.Config(header)

    # act
    with pytest.raises(InvalidPythonException) as invalid_python_exception:
        panaetius.set_config(config, "invalid_python")

    # assert
    assert str(invalid_python_exception.value) == "a string without quotes is not valid Python."

    # cleanup
    del os.environ[f"{header.upper()}_INVALID_PYTHON"]
