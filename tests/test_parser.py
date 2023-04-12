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
])
def test_parser_must_handle_ontology(text, result):
    parser = make_parser()
    parser.parse(text)
    assert parser.result == result
