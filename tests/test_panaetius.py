import os

from panaetius import Config, set_config

if __name__ == "__main__":
    os.environ["PANAETIUS_TEST_PATH"] = "/usr/local"
    print(os.environ.get("PANAETIUS_TEST_PATH"))
    os.environ[
        "PANAETIUS_TEST_TOML_POINTS"
    ] = "[ { x = 1, y = 2, z = 3 }, { x = 7, y = 8, z = 9 }, { x = 2, y = 4, z = 8 }]"
    c = Config("panaetius_test")

    set_config(c, key="path", default="some path")
    set_config(c, key="top", default="some top")
    set_config(c, key="logging.path", default="some logging path")
    set_config(c, key="nonexistent.item", default="some nonexistent item")
    set_config(c, key="nonexistent.item")
    set_config(c, key="toml.points", coerce=True)
    set_config(c, key="toml.points_config")
    set_config(c, key="float", default=2.0)
    set_config(c, key="float_str", default="2.0")

    print(c)
    pass
