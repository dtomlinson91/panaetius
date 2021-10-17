import pytest


@pytest.fixture()
def header():
    return "panaetius_testing"


@pytest.fixture()
def testing_config_contents():
    return {
        "panaetius_testing": {
            "some_top_string": "some_top_value",
            "second": {
                "some_second_string": "some_second_value",
                "some_second_int": 1,
                "some_second_float": 1.0,
                "some_second_list": ["some", "second", "value"],
                "some_second_table": {"first": ["some", "first", "value"]},
                "some_second_table_bools": {"bool": [True, False]},
            },
        }
    }
