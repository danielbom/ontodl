import pytest
from ontodl import create_lexer, create_parser


def make_parser():
    lexer = create_lexer()
    parser = create_parser(out='json')
    parser.lexer = lexer
    return parser


@pytest.mark.parametrize("text,result", [
    ['''Ontologia T conceitos {} individuos {} relacoes {} triplos {}.''', {
        'ontology': 'T',
        'concepts': {},
        'individuals': [],
        'relations': [],
        'triples': [],
    }],
    ['''Ontologia T conceitos { a } individuos { b } relacoes { c } triplos { b = c => a; }.''', {
        'ontology': 'T',
        'concepts': {'a': {}},
        'individuals': ["b"],
        'relations': ['c'],
        'triples': [{'concept': 'a', 'individual': 'b', 'properties': {}, 'relation': 'c'}],
    }],
    ['''Ontologia T conceitos { a [f: date] } individuos { b } relacoes { c } triplos { b = c => a[f=2020-10-10]; }.''', {
        'ontology': 'T',
        'concepts': {'a': {'f': 'date'}},
        'individuals': ["b"],
        'relations': ['c'],
        'triples': [{'concept': 'a', 'individual': 'b', 'properties': {"f": ['2020-10-10', 'date']}, 'relation': 'c'}],
    }],
    ['''Ontologia T conceitos { a [f: date, g: boolean] } individuos { b } relacoes { c } triplos { b = c => a[f=2020-10-10, g=true]; }.''', {
        'ontology': 'T',
        'concepts': {'a': {'f': 'date', 'g': 'boolean'}},
        'individuals': ["b"],
        'relations': ['c'],
        'triples': [{'concept': 'a', 'individual': 'b', 'properties': {"f": ['2020-10-10', 'date'], 'g': ['true', 'boolean']}, 'relation': 'c'}],
    }],
    ['''Ontologia T conceitos { a [f: date, g: boolean], b } individuos { } relacoes { } triplos { b = isa => a; }.''', {
        'ontology': 'T',
        'concepts': {'a': {'f': 'date', 'g': 'boolean'}, 'b': {}},
        'individuals': [],
        'relations': [],
        'triples': [{'concept': 'a', 'individual': 'b', 'properties': {}, 'relation': 'isa'}],
    }],
])
def test_parser_must_handle_ontology(text, result):
    parser = make_parser()
    parser.parse(text)
    assert parser.result == result
