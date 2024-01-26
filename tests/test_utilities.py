import pytest
from pathlib import Path

from bart.utilites import (
    get_next_doc_number,
    get_valid_pathname
)


def test_get_valid_pathname():
    """
    Ensures that various undesirable characters are flattened to mere dashes
    and are lowercase
    """
    test_name = "ThIs! Title, an example. Or: (also) \\test/case"

    assert get_valid_pathname(test_name) == \
        "this-title-an-example-or-also-test-case"


class TestGetNextDocNumber:
    """
    Tests around the "next doc" getter
    """

    def test_get_next_doc_number_no_last(self):
        """
        If there is no last doc (i.e., it's a new project), it should be padded
        per level
        """
        # special "1  case
        level_1 = get_next_doc_number(None, 1, 0)
        assert level_1 == "00"

        # expected subsequent cases
        level_2 = get_next_doc_number(None, 2, 0)
        assert level_2 == "00"

        level_3 = get_next_doc_number(None, 3, 0)
        assert level_3 == "000"

    @pytest.mark.parametrize("case,expected",[
           (1, "01"),
           (2, "01"),
           (3, "001"),
        ])
    def test_get_next_doc_number_levels(self, case, expected):
        """
        Tests other cases! See parametrize for expectations.
        """
        last_doc = Path('00-example.adoc') 
        numbering = get_next_doc_number(last_doc, case, 1)
        assert numbering == expected

    @pytest.mark.parametrize("case,expected",[
           (1, "11"),
           (2, "20"),
           (3, "110"),
        ])
    def test_get_next_doc_position_levels(self, case, expected):
        """
        Tests position levels, note that we're duplicating the project levels so
        the case doesn't break (this is accounted for in the project function)
        """
        last_doc = Path('10-example.adoc') 
        numbering = get_next_doc_number(last_doc, case, (10 ** (case - 1)))
        assert numbering == expected

