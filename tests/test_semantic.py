import pytest
from ontodl import create_parser, JsonTransformer, validate_json


@pytest.mark.parametrize("text,error", [
    ['''Ontologia T conceitos {} individuos {} relacoes { isa } triplos {}.''',
        "Relation 'isa' is a builtin relation"],
    ['''Ontologia T conceitos {} individuos {} relacoes { iof } triplos {}.''',
        "Relation 'iof' is a builtin relation"],
    ['''Ontologia T conceitos {} individuos {} relacoes {} triplos { a = iof => A; }.''',
        "Relation 'iof' must have an individual as the 1st argument."],
    ['''Ontologia T conceitos {} individuos { a } relacoes {} triplos { a = iof => A; }.''',
        "Relation 'iof' must have a concepts as the 2nd argument."],
    ['''Ontologia T conceitos { A[name:string] } individuos { a } relacoes {} triplos { a = iof => A; }.''',
        "Property 'A.name' is not defined in triple"],
    ['''Ontologia T conceitos { A[name:string] } individuos { a } relacoes {} triplos { a = iof => A[name=10]; }.''',
        "Property 'A.name' is of type 'string', but got type 'number' in triple"],
    ['''Ontologia T conceitos { A } individuos { a } relacoes {} triplos { a = iof => A[name=10]; }.''',
        "Property 'A.name' is not defined in concept"],
    ['''Ontologia T conceitos {} individuos { a } relacoes { a } triplos {}.''',
        "Individual, relation and concept have overlapping keys"],
    ['''Ontologia T conceitos { a[f:string] } individuos { b } relacoes { } triplos { b = isa => a; }.''',
        "Relation 'isa' of must have only concepts."],
    ['''Ontologia T conceitos { a[f:string], b } individuos { } relacoes { } triplos { b = isa => a[name="X"]; }.''',
        "Only relation 'iof' must have properties."],
])
def test_ontology_must_be_validated_for_dot_legacy(text, error):
    parser = create_parser(transformer=JsonTransformer())
    try:
        json = parser.parse(text)
        validate_json(json)
        assert False
    except Exception as e:
        assert str(e) == error
