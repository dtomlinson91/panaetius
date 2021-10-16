import os

from panaetius import Config, set_config

if __name__ == "__main__":
    os.environ["PANAETIUS_TEST_PATH"] = "/usr/local"
    print(os.environ.get("PANAETIUS_TEST_PATH"))
    os.environ[
        "PANAETIUS_TEST_TOML_POINTS"
    ] = "[ { x = 1, y = 2, z = 3 }, { x = 7, y = 8, z = 9 }, { x = 2, y = 4, z = 8 }]"
    c = Config("panaetius_test")
    # print(c.config)
    # c.get_value("path", "some path")
    # c.get_value("top", "str")
    # c.get_value("logging.path", "str")
    # c.get_value("nonexistent.item", "some default value")
    set_config(c, key="path", default="some path")
    set_config(c, key="top", default="some top")
    set_config(c, key="logging.path", default="some logging path")
    set_config(c, key="nonexistent.item", default="some nonexistent item")
    set_config(c, key="nonexistent.item")
    set_config(c, key="toml.points")
    print(c)
    pass
