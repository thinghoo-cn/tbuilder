from builder.core.entity.version import Version


def test_version_parse():
    content = "0.10.0.202310"
    v = Version.parse_str(content=content)
    assert v.get_full() == "v0.10.0.202310"
