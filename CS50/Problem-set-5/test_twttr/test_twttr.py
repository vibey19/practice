from twttr import shorten


def test_lowercase():
    assert shorten("twitter") == "twttr"
    assert shorten("hello") == "hll"


def test_uppercase():
    assert shorten("TWITTER") == "TWTTR"
    assert shorten("HELLO") == "HLL"


def test_mixed_case():
    assert shorten("TwItTeR") == "TwtTR"


def test_numbers_and_symbols():
    assert shorten("h3ll0!") == "h3ll0!"
    assert shorten("CS50") == "CS50"
    assert shorten("hello, world!") == "hll, wrld!"


def test_no_vowels():
    assert shorten("rhythm") == "rhythm"


def test_empty_string():
    assert shorten("") == ""