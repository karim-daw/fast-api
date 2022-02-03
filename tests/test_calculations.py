import pytest
from app.calculations import add

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,3,10),
    (4,5,9)
]

)
def test_add_2_items(num1, num2, expected) -> None:
    """ Total of empty list should be 4"""
    assert add(num1,num2) == expected
