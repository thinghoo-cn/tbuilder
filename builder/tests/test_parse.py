from builder.entity.version import Version


def test_version_parse():
    content = "0.11.0"
    v = Version.parse_str(content=content)
    assert v.get_full() == "v0.11.0"
