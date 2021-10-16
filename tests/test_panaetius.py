import os

from panaetius import Config, set_config

if __name__ == "__main__":
    os.environ["PANAETIUS_TEST_PATH"] = "/usr/local"
    os.environ["PANAETIUS_TEST_BOOL"] = "true"
    print(os.environ.get("PANAETIUS_TEST_PATH"))
    # os.environ[
    #     "PANAETIUS_TEST_TOML_POINTS"
    # ] = "[ { x = 1, y = 2, z = 3 }, { x = 7, y = 8, z = 9 }, { x = 2, y = 4, z = 8 }]"

    os.environ["PANAETIUS_TEST_NOC_PATH"] = "/usr/locals"
    os.environ["PANAETIUS_TEST_NOC_FLOAT"] = "2.0"
    os.environ["PANAETIUS_TEST_NOC_BOOL"] = "true"
    os.environ["PANAETIUS_TEST_NOC_EMBEDDED_PATH"] = "/usr/local"
    os.environ["PANAETIUS_TEST_NOC_EMBEDDED_FLOAT"] = "2.0"
    os.environ["PANAETIUS_TEST_NOC_EMBEDDED_BOOL"] = "true"

    c = Config("panaetius_test")
    # c = Config("panaetius_test_noc")

    set_config(c, key="toml.points", coerce=True)
    set_config(c, key="path", default="some path")
    set_config(c, key="top", default="some top")
    set_config(c, key="logging.path", default="some logging path")
    set_config(c, key="nonexistent.item", default="some nonexistent item")
    set_config(c, key="nonexistent.item")
    # FIXME: this isn't working after the refactor...
    set_config(c, key="toml.points_config")
    set_config(c, key="float", default=2.0)
    set_config(c, key="float_str", default="2.0")
    set_config(c, key="bool", coerce=True)
    set_config(c, key="noexistbool", default=False)
    set_config(c, key="middle.middle")

    # set_config(c, key="path")
    # set_config(c, key="float", coerce=True)
    # set_config(c, key="bool", coerce=True)
    # set_config(c, key="noexiststr", default="2.0")
    # set_config(c, key="noexistfloat", default=2.0)
    # set_config(c, key="noexistbool", default=False)

    set_config(c, key="embedded.path")
    set_config(c, key="embedded.float", coerce=True)
    set_config(c, key="embedded.bool", coerce=True)
    set_config(c, key="embedded.noexiststr", default="2.0")
    set_config(c, key="embedded.noexistfloat", default=2.0)
    set_config(c, key="embedded.noexistbool", default=False)

    print(c)
    pass
