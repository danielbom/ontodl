from ontodl import create_parser
import pytest


@pytest.mark.parametrize("text", [
    'true',
    'false',
])
def test_parser_must_handle_boolean_token(text):
    parser = create_parser(start=["boolean"])
    parser.parse(text, start="boolean")


@pytest.mark.parametrize("text", [
    '2020-01-01',
    '2020-01-01 00:00:00',
    '2020-01-01T00:00:00',
    '2020-01-01T00:00:00.000',
    '2020-01-01T00:00:00.000Z',
    '2020-01-01T00:00:00.000+01:00',
    '2020-01-01T00:00:00.000-01:00',
])
def test_parser_must_handle_date_token(text):
    parser = create_parser(start=["date"])
    parser.parse(text)


@pytest.mark.parametrize("text", [
    '123',
    '123.456',
    '123.456e789',
    '123e789',
    '123e+789',
    '123e-789',
])
def test_parser_must_handle_number_token(text):
    parser = create_parser(start=["number"])
    parser.parse(text)


@pytest.mark.parametrize("text", [
    'abc',
    '_abc',
    '_123',
    '_áé'
])
def test_parser_must_handle_id_token(text):
    parser = create_parser(start=["id"])
    parser.parse(text)


@pytest.mark.parametrize("text", [
    '"abc"',
    '"asda adas"',
    '"123 123"',
])
def test_parser_must_handle_string_token(text):
    parser = create_parser(start=["string"])
    parser.parse(text)
