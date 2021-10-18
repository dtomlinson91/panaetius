import os

from panaetius import Config, set_config, set_logger, SimpleLogger

from panaetius.logging import AdvancedLogger

if __name__ == "__main__":
    os.environ["PANAETIUS_TEST_PATH"] = '"/usr/local"'
    os.environ["PANAETIUS_TEST_BOOL"] = "True"
    # print(os.environ.get("PANAETIUS_TEST_PATH"))
    # os.environ[
    #     "PANAETIUS_TEST_TOML_POINTS"
    # ] = "[ { x = 1, y = 2, z = 3 }, { x = 7, y = 8, z = 9 }, { x = 2, y = 4, z = 8 }]"

    os.environ["PANAETIUS_TEST_NOC_PATH"] = '"/usr/locals"'
    os.environ["PANAETIUS_TEST_NOC_FLOAT"] = "2.0"
    os.environ["PANAETIUS_TEST_NOC_BOOL"] = "True"
    os.environ["PANAETIUS_TEST_NOC_EMBEDDED_PATH"] = '"/usr/local"'
    os.environ["PANAETIUS_TEST_NOC_EMBEDDED_FLOAT"] = "2.0"
    os.environ["PANAETIUS_TEST_NOC_EMBEDDED_BOOL"] = "True"

    c = Config("panaetius_test")
    # c = Config("panaetius_test_noc")

    set_config(c, key="toml.points")
    set_config(c, key="path", default="some path")
    set_config(c, key="top", default="some top")
    set_config(c, key="logging.path")
    set_config(c, key="nonexistent.item", default="some nonexistent item")
    set_config(c, key="nonexistent.item")
    set_config(c, key="toml.points_config")
    set_config(c, key="float")
    set_config(c, key="float_str", default="2.0")
    set_config(c, key="bool")
    set_config(c, key="noexistbool", default=False)
    set_config(c, key="middle.middle")

    # set_config(c, key="path")
    # set_config(c, key="float")
    # set_config(c, key="bool")
    # set_config(c, key="noexiststr", default="2.0")
    # set_config(c, key="noexistfloat", default=2.0)
    # set_config(c, key="noexistbool", default=False)

    set_config(c, key="embedded.path")
    set_config(c, key="embedded.float")
    set_config(c, key="embedded.bool")
    set_config(c, key="embedded.noexiststr", default="2.0")
    set_config(c, key="embedded.noexistfloat", default=2.0)
    set_config(c, key="embedded.noexistbool", default=False)

    # logger = set_logger(c, SimpleLogger())
    logger = set_logger(c, SimpleLogger(logging_level="DEBUG"))
    logger.info("some logging message")
    logger.debug("debugging message")
    # for i in dir(c):
    #     logger.debug(i + ": " + str(getattr(c, i)) + " - " + str(type(getattr(c, i))))
