from shopping_cart import calculate_total, apply_tax

def test_calculate_total_no_discount():
    assert calculate_total([10, 20, 30]) == 60

def test_calculate_total_with_discount():
    assert calculate_total([100], discount_percent=10) == 90

def test_apply_tax():
    assert round(apply_tax(100), 2) == 108.0
