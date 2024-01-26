from bart.utilites import get_valid_pathname


def test_get_valid_pathname():
    """
    Ensures that various undesirable characters are flattened to mere dashes
    and are lowercase
    """
    test_name = "ThIs! Title, an example. Or: (also) \\test/case"

    assert get_valid_pathname(test_name) == \
        "this-title-an-example-or-also-test-case"
