import pytest
from ontodl import create_lexer, create_parser


def make_parser(out):
    lexer = create_lexer()
    parser = create_parser(out=out)
    parser.lexer = lexer
    return parser


@pytest.mark.parametrize("text,error", [
    ['''Ontologia T conceitos {} individuos {} relacoes { isa } triplos {}.''',
        "Relation 'isa' is a builtin relation"],
    ['''Ontologia T conceitos {} individuos {} relacoes { iof } triplos {}.''',
        "Relation 'iof' is a builtin relation"],
    ['''Ontologia T conceitos {} individuos {} relacoes {} triplos { a = iof => A; }.''',
        "Individual 'a' is not defined"],
    ['''Ontologia T conceitos {} individuos { a } relacoes {} triplos { a = iof => A; }.''',
        "Concept 'A' is not defined"],
    ['''Ontologia T conceitos { A[name:string] } individuos { a } relacoes {} triplos { a = iof => A; }.''',
        "Property 'A.name' is not defined in triple"],
    ['''Ontologia T conceitos { A[name:string] } individuos { a } relacoes {} triplos { a = iof => A[name=10]; }.''',
        "Property 'A.name' is of type 'string', but got type 'number' in triple"],
    ['''Ontologia T conceitos { A } individuos { a } relacoes {} triplos { a = iof => A[name=10]; }.''',
        "Property 'A.name' is not defined in concept"],
    ['''Ontologia T conceitos {} individuos { a } relacoes { a } triplos {}.''',
        "Individual, relation and concept have overlapping keys"],
])
def test_ontology_must_be_validated_for_json_dot(text, error):
    parser = make_parser('json_dot')
    try:
        parser.parse(text)
        parser.complete()
        print(parser.result)
        assert False
    except Exception as e:
        assert str(e) == error


@pytest.mark.parametrize("text,error", [
    ['''Ontologia T conceitos {} individuos {} relacoes { isa } triplos {}.''',
        'Entry with name "isa" already exists as relation.'],
    ['''Ontologia T conceitos {} individuos {} relacoes { iof } triplos {}.''',
        'Entry with name "iof" already exists as relation.'],
    ['''Ontologia T conceitos {} individuos {} relacoes {} triplos { a = iof => A; }.''',
        'Individual "a" does not exist.'],
    ['''Ontologia T conceitos {} individuos { a } relacoes {} triplos { a = iof => A; }.''',
        'Concept "A" does not exist.'],
    ['''Ontologia T conceitos { A[name:string] } individuos { a } relacoes {} triplos { a = iof => A; }.''',
        'Attribute "name" of concept "A" is not set.'],
    ['''Ontologia T conceitos { A[name:string] } individuos { a } relacoes {} triplos { a = iof => A[name=10]; }.''',
        'Attribute "name" of concept "A" is of type "string", not "number".'],
    ['''Ontologia T conceitos { A } individuos { a } relacoes {} triplos { a = iof => A[name=10]; }.''',
        'Concept "A" does not have attribute "name".'],
    ['''Ontologia T conceitos {} individuos { a } relacoes { a } triplos {}.''',
        'Entry with name "a" already exists as individual.'],
])
def test_ontology_must_be_validated_for_dot(text, error):
    parser = make_parser('dot')
    try:
        parser.parse(text)
        parser.complete()
        print(parser.result)
        assert False
    except Exception as e:
        assert str(e) == error
