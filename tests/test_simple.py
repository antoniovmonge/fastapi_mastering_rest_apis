def test_add_two():
    x = 1
    y = 2
    assert x + y == 3


def test_dict_contains():
    d = {"a": 1, "b": 2}
    assert "a" in d
    assert "c" not in d
