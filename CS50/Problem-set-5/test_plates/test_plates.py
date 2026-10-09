
from plates import is_valid


def test_length():
    assert is_valid("AB") == True
    assert is_valid("ABC123") == True
    assert is_valid("A") == False
    assert is_valid("ABCDEFG") == False


def test_start_with_two_letters():
    assert is_valid("AA123") == True
    assert is_valid("1A22") == False
    assert is_valid("A122") == False


def test_numbers_at_end():
    assert is_valid("AAA222") == True
    assert is_valid("AA22") == True
    assert is_valid("AAA22A") == False
    assert is_valid("AA2A") == False


def test_first_number_not_zero():
    assert is_valid("CS50") == True
    assert is_valid("CS05") == False
    assert is_valid("AA012") == False


def test_alphanumeric_only():
    assert is_valid("AA 22") == False
    assert is_valid("AA.22") == False
    assert is_valid("AA!22") == False


def test_letters_only():
    assert is_valid("HELLO") == True
    assert is_valid("CS") == True