from ..conf import Config, Version


def test_load_config():
    c: Config = Config.load_config()
    assert c.get_version() == Version(0, 1, 0)
    assert c.prefix == "qms-compose"
