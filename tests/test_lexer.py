from ontodl import create_lexer
import pytest


def test_lexer_must_be_defined():
    lexer = create_lexer()
    assert lexer is not None


@pytest.mark.parametrize("text,typ", [
    ('Ontologia', 'ONTOLOGY'),
    ('Ontology', 'ONTOLOGY'),
    ('concepts', 'CONCEPTS'),
    ('conceitos', 'CONCEPTS'),
    ('individuals', 'INDIVIDUALS'),
    ('individuos', 'INDIVIDUALS'),
    ('relations', 'RELATIONS'),
    ('relacoes', 'RELATIONS'),
    ('triples', 'TRIPLES'),
    ('triplos', 'TRIPLES'),
    ('string', 'TYPES'),
    ('integer', 'TYPES'),
    ('float', 'TYPES'),
    ('boolean', 'TYPES'),
    ('date', 'TYPES'),
    ('=>', 'IMPLIES'),
])
def test_lexer_must_handle_named_tokens(text, typ):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == typ
    assert token.value == text


@pytest.mark.parametrize("text", [
    'true',
    'false',
])
def test_lexer_must_handle_boolean_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == 'BOOLEAN'
    assert token.value == text


@pytest.mark.parametrize("text", [
    '2020-01-01',
    '2020-01-01 00:00:00',
    '2020-01-01T00:00:00',
    '2020-01-01T00:00:00.000',
    '2020-01-01T00:00:00.000Z',
    '2020-01-01T00:00:00.000+01:00',
    '2020-01-01T00:00:00.000-01:00',
])
def test_lexer_must_handle_date_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == 'DATE'
    assert token.value == text


@pytest.mark.parametrize("text", [
    '123',
    '123.456',
    '123.456e789',
    '123e789',
    '123e+789',
    '123e-789',
])
def test_lexer_must_handle_number_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == 'NUMBER'
    assert token.value == text


@pytest.mark.parametrize("text", [
    'abc',
    '_abc',
    '_123',
    '_áé'
])
def test_lexer_must_handle_id_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == 'ID'
    assert token.value == text


@pytest.mark.parametrize("text", [
    '"abc"',
    '"asda adas"',
    '"123 123"',
])
def test_lexer_must_handle_string_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == 'STRING'
    assert token.value == text


@pytest.mark.parametrize("text", [
    '{', '}', '[', ']', ':', ';', ',', '.',
])
def test_lexer_must_handle_literal_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token.type == text
    assert token.value == text


@pytest.mark.parametrize("text", [
    ' ',
    '\t',
    '\r',
])
def test_lexer_must_handle_ignored_token(text):
    lexer = create_lexer()
    lexer.input(text)
    token = lexer.token()
    assert token is None
