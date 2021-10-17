import panaetius


def test_set_config(header, shared_datadir):
    # arrange
    config_path = str(shared_datadir / "without_logging")

    # act
    config = panaetius.Config(header, config_path)
    panaetius.set_config(config, "some_top_string")

    # assert
    assert getattr(config, "some_top_string") == "some_top_value"
