import pytest

from web_messaging.blueprints.texting.views import validate_phone


def test_validate_phone_one():
    assert True == validate_phone('0624180314')

def test_validate_phone_two():
    assert True == validate_phone('0799098736')

def test_too_long_phone():
    assert False == validate_phone('06241803144')


def test_invalid_phone_digit():
    assert False == validate_phone('0989764555')
