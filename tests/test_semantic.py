import pytest
from ontodl import create_lexer, create_parser


def make_parser():
    lexer = create_lexer()
    parser = create_parser(out='dot')
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
def test_ontology_must_be_validated(text, error):
    parser = make_parser()
    try:
        parser.parse(text)
        parser.complete()
        print(parser.result)
        assert False
    except Exception as e:
        assert str(e) == error
