from bank import value


def test_hello():
    assert value("hello") == 0
    assert value("hello, world") == 0


def test_h():
    assert value("hi") == 20
    assert value("hey") == 20


def test_other():
    assert value("good morning") == 100
    assert value("greetings") == 100


def test_case_insensitive():
    assert value("HELLO") == 0
    assert value("Hello") == 0
    assert value("HEY") == 20