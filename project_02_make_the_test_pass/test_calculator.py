from calculator import add, multiply, is_even

def test_add():
    assert add(2, 3) == 5

def test_multiply():
    assert multiply(2, 3) == 6

def test_is_even():
    assert is_even(4) == True
