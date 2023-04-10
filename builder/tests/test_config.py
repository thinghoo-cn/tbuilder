from builder.core.conf import Config, Version


def test_load_config():
    c: Config = Config.load_config()
    assert c.get_version() == Version(0, 10, 0, date=202304)
    assert c.prefix == "mes-compose"


def test_write_back():
    import shutil
    from datetime import datetime

    shutil.copy('./config-example.yml', './config.yml')
    c: Config = Config.load_config()
    mydate = datetime.now().date()
    c.name = f'{mydate}-{c.name}'
    c.write_back()

    c2 = Config.load_config()
    assert c2.name == c.name
