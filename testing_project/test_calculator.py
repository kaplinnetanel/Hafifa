import pytest 
from calculator import add
from unittest.mock import patch  
from products import is_expennsive
# parametrize
# @pytest.mark.parametrize(
#        "a,b,expected", 
#        [
#            (2,3,5),
#            (10,5,15),
#            (-2,2,9)
#        ] 
# )
# def test_add(a, b, expected):
#     assert add(a,b)  == expected

# fixture
# @pytest.fixture
# def numbers():
#     return [10,20,30]

# def test_sum(numbers):
#     assert sum(numbers) == 60

# Mock

def test_is_expensive():
    with patch("products.get_product_from_db") as m_db:
        m_db.return_value = {
            "id" :1,
            "price": 150
        }

        result = is_expennsive(1)

        assert result == True
        m_db.assert_called_once_with(1)
