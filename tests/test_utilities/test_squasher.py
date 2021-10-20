import pytest

from panaetius import utilities


def test_squashed_data(squashed_data, squashed_data_result):
    # act
    squashed_data_pre_squashed = utilities.squasher.Squash(squashed_data).as_dict

    # assert
    assert squashed_data_pre_squashed == squashed_data_result


@pytest.fixture
def squashed_data():
    return {
        "destination_addresses": [
            "Washington, DC, USA",
            "Philadelphia, PA, USA",
            "Santa Barbara, CA, USA",
            "Miami, FL, USA",
            "Austin, TX, USA",
            "Napa County, CA, USA",
        ],
        "origin_addresses": ["New York, NY, USA"],
        "rows": [
            {
                "elements": [
                    {
                        "distance": {"text": "227 mi", "value": 365468},
                        "duration": {
                            "text": "3 hours 54 mins",
                            "value": 14064,
                        },
                        "status": "OK",
                    },
                    {
                        "distance": {"text": "94.6 mi", "value": 152193},
                        "duration": {"text": "1 hour 44 mins", "value": 6227},
                        "status": "OK",
                    },
                    {
                        "distance": {"text": "2,878 mi", "value": 4632197},
                        "duration": {
                            "text": "1 day 18 hours",
                            "value": 151772,
                        },
                        "status": "OK",
                    },
                    {
                        "distance": {"text": "1,286 mi", "value": 2069031},
                        "duration": {
                            "text": "18 hours 43 mins",
                            "value": 67405,
                        },
                        "status": "OK",
                    },
                    {
                        "distance": {"text": "1,742 mi", "value": 2802972},
                        "duration": {"text": "1 day 2 hours", "value": 93070},
                        "status": "OK",
                    },
                    {
                        "distance": {"text": "2,871 mi", "value": 4620514},
                        "duration": {
                            "text": "1 day 18 hours",
                            "value": 152913,
                        },
                        "status": "OK",
                    },
                ]
            }
        ],
        "status": "OK",
    }


@pytest.fixture
def squashed_data_result():
    return {
        "destination_addresses_0": "Washington, DC, USA",
        "destination_addresses_1": "Philadelphia, PA, USA",
        "destination_addresses_2": "Santa Barbara, CA, USA",
        "destination_addresses_3": "Miami, FL, USA",
        "destination_addresses_4": "Austin, TX, USA",
        "destination_addresses_5": "Napa County, CA, USA",
        "origin_addresses_0": "New York, NY, USA",
        "rows_0_elements_0_distance_text": "227 mi",
        "rows_0_elements_0_distance_value": 365468,
        "rows_0_elements_0_duration_text": "3 hours 54 mins",
        "rows_0_elements_0_duration_value": 14064,
        "rows_0_elements_0_status": "OK",
        "rows_0_elements_1_distance_text": "94.6 mi",
        "rows_0_elements_1_distance_value": 152193,
        "rows_0_elements_1_duration_text": "1 hour 44 mins",
        "rows_0_elements_1_duration_value": 6227,
        "rows_0_elements_1_status": "OK",
        "rows_0_elements_2_distance_text": "2,878 mi",
        "rows_0_elements_2_distance_value": 4632197,
        "rows_0_elements_2_duration_text": "1 day 18 hours",
        "rows_0_elements_2_duration_value": 151772,
        "rows_0_elements_2_status": "OK",
        "rows_0_elements_3_distance_text": "1,286 mi",
        "rows_0_elements_3_distance_value": 2069031,
        "rows_0_elements_3_duration_text": "18 hours 43 mins",
        "rows_0_elements_3_duration_value": 67405,
        "rows_0_elements_3_status": "OK",
        "rows_0_elements_4_distance_text": "1,742 mi",
        "rows_0_elements_4_distance_value": 2802972,
        "rows_0_elements_4_duration_text": "1 day 2 hours",
        "rows_0_elements_4_duration_value": 93070,
        "rows_0_elements_4_status": "OK",
        "rows_0_elements_5_distance_text": "2,871 mi",
        "rows_0_elements_5_distance_value": 4620514,
        "rows_0_elements_5_duration_text": "1 day 18 hours",
        "rows_0_elements_5_duration_value": 152913,
        "rows_0_elements_5_status": "OK",
        "status": "OK",
    }
