from deadlock_middleware import name


def test_name_is_same_as_module():
    assert name == "deadlock_middleware"
