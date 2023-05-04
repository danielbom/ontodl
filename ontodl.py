'''
# ONTODL Language Specification

This is the specification for the ONTODL language. ONTODL is a language for describing ontologies.

You can try an online version of ONTODL to DOT [here](https://webontodl.epl.di.uminho.pt/).

You can find the source code in [Github](https://github.com/danielbom/ontodl).

# Get started

To use this script, you need have lark installed.

```
# create a virtual environment (optional)
python -m venv venv
source venv/bin/activate    # linux
./venv/Scripts/activate.ps1 # windows powershell

# install lark
pip install lark
```

Show the help:

```bash
python3 ontodl.py --help
python3 ontodl.py -h
```

Use some samples to test:

```bash
# default format is dot
python3 ontodl.py samples/ontodl_sample1.ontodl --format dot
python3 ontodl.py samples/ontodl_sample2.ontodl --format prolog
python3 ontodl.py samples/ontodl_sample2.ontodl --format owl # Web Ontology Language
python3 ontodl.py samples/ontodl_sample1.ontodl --format json
python3 ontodl.py samples/ontodl_sample2.ontodl --format log
python3 ontodl.py samples/ontodl_sample2.ontodl --format tree
```

Looks for the tokenization of the input:

```bash
python3 ontodl.py samples/ontodl_sample1.ontodl --tokenize
python3 ontodl.py samples/ontodl_sample2.ontodl --tokenize
```

Looks the grammar

```bash	
python3 ontodl.py --grammar
```

'''
from lark import Transformer

grammar = r"""
ONTOLOGY    : "Ontology" | "Ontologia"
CONCEPTS    : "concepts" | "conceitos"
INDIVIDUALS : "individuals" | "individuos"
RELATIONS   : "relations" | "relacoes"
TRIPLES     : "triples" | "triplos"

TYPES : "string" | "integer" | "float" | "boolean" | "date"

BOOLEAN : "true" | "false"
ID      : /[a-zA-ZÀ-ÖØ-öø-ÿ_][a-zA-ZÀ-ÖØ-öø-ÿ0-9_]*/
DATE    : /\d{4}-\d{2}-\d{2}([T ](\d{2}:\d{2}:\d{2}(\.\d+)?(\.0+)?)(Z|(\+|-)\d{2}:\d{2})?)?/
NUMBER  : /-?\d+(\.\d+)?([eE][+-]?\d+)?/
STRING  : /\"[^"]*\"/
COMMENT : /%.*/

start           : ontology concepts individuals relations triples end
end             : "."

ontology        : ONTOLOGY id

concepts        : CONCEPTS "{" concept_list "}"
concept_list    : _sep_by{",", concept}
concept         : id "[" attribute_list "]"
                | id
attribute_list  : _sep_by{",", attribute}
attribute       : id ":" type

individuals     : INDIVIDUALS "{" individual_list "}"
individual_list : _sep_by{",", individual}
individual      : id

relations       : RELATIONS "{" relation_list "}"
relation_list   : _sep_by{",", relation}
relation        : id

triples         : TRIPLES "{" triple_list "}"
triple_list     : triple (triple)*
                | 
triple          : id "=" id "=>" entity ";"
entity          : id "[" properties_list "]"
                | id
properties_list : _sep_by{",", property}
property        : id "=" value

value           : number
                | boolean
                | string
                | date
number          : NUMBER
boolean         : BOOLEAN
string          : STRING
date            : DATE
type            : TYPES
id              : ID
                | STRING

_sep_by{sep, item} : item (sep item)* 
                   | 

%import common.WS
%ignore WS | COMMENT
"""


class JsonTransformer(Transformer):
    def start(self, items):
        return {
            "ontology": items[0],
            "concepts": items[1],
            "individuals": items[2],
            "relations": items[3],
            "triples": items[4]
        }

    # Ontology
    def ontology(self, items):
        return items[1]

    # Concepts
    def concepts(self, items):
        return dict(items[1])

    def concept_list(self, items):
        return items

    def concept(self, items):
        if len(items) == 1:
            return [items[0], {}]
        return [items[0], dict(items[1])]

    def attribute_list(self, items):
        return items

    def attribute(self, items):
        return [items[0], items[1]]

    # Individuals
    def individuals(self, items):
        return items[1]

    def individual_list(self, items):
        return items

    def individual(self, items):
        return items[0]

    # Relations
    def relations(self, items):
        return items[1]

    def relation_list(self, items):
        return items

    def relation(self, items):
        return items[0]

    # Triples
    def triples(self, items):
        return items[1]

    def triple_list(self, items):
        return items

    def triple(self, items):
        return {
            "individual": items[0],
            "relation": items[1],
            "concept": items[2]['concept'],
            "properties": items[2]['properties']
        }

    def entity(self, items):
        if len(items) == 1:
            return {"concept": items[0], "properties": {}}
        return {"concept": items[0], "properties": dict(items[1])}

    def properties_list(self, items):
        return items

    def property(self, items):
        return [items[0], items[1]]

    def value(self, items):
        return items[0]

    # Atoms
    def number(self, items):
        return [items[0].value, 'number']

    def boolean(self, items):
        return [items[0].value, 'boolean']

    def string(self, items):
        return [items[0].value, 'string']

    def date(self, items):
        return [items[0].value, 'date']

    def type(self, items):
        return items[0].value

    def id(self, items):
        return items[0].value.strip('"')


def validate_json(json):
    builtin_relations = ['isa', 'iof']
    for relation in json['relations']:
        if relation in builtin_relations:
            raise Exception(f"Relation '{relation}' is a builtin relation")
    # Individual, relation and concept must have disjoint keys
    parts = ['individuals', 'relations', 'concepts']
    keys_count = 0
    all_keys = set()
    for part in parts:
        if isinstance(json[part], dict):
            all_keys |= json[part].keys()
            keys_count += len(json[part].keys())
        else:
            all_keys |= set(json[part])
            keys_count += len(json[part])
    if len(all_keys) != keys_count:
        raise Exception(
            f"Individual, relation and concept have overlapping keys")

    all_relations = builtin_relations + json['relations']

    for triple in json['triples']:
        if triple['relation'] != 'iof':
            if len(triple['properties']) > 0:
                raise Exception(
                    "Only relation 'iof' must have properties.")
        # Relations 'isa' must have concepts as arguments without properties
        if triple['relation'] == 'isa':
            relation = f"{triple['individual']} = isa => {triple['concept']}"
            if triple['concept'] not in json['concepts']:
                raise Exception(
                    "Relation 'isa' of must have only concepts.")
            if triple['individual'] not in json['concepts']:
                raise Exception(
                    "Relation 'isa' of must have only concepts.")
            continue
        if triple['relation'] == 'iof':
            if triple['individual'] not in json['individuals']:
                raise Exception(
                    "Relation 'iof' must have an individual as the 1st argument.")
            if triple['concept'] not in json['concepts']:
                raise Exception(
                    "Relation 'iof' must have a concepts as the 2nd argument.")
            concept_name = triple['concept']
            concept = json['concepts'][concept_name]
            properties = triple['properties']
            for prop, typ in properties.items():
                typ = typ[1]
                if prop not in concept:
                    raise Exception(
                        f"Property '{concept_name}.{prop}' is not defined in concept")
                if typ != concept[prop]:
                    raise Exception(
                        f"Property '{concept_name}.{prop}' is of type '{concept[prop]}', but got type '{typ}' in triple")
            # Properties must be defined in triple
            for prop, typ in concept.items():
                if prop not in properties:
                    raise Exception(
                        f"Property '{concept_name}.{prop}' is not defined in triple")
            continue
        # Individual must be defined
        individual_defined = triple['individual'] in json['individuals'] or triple['individual'] in json['concepts']
        if not individual_defined:
            raise Exception(
                f"Individual '{triple['individual']}' is not defined")
        # Relation must be defined
        if triple['relation'] not in all_relations:
            raise Exception(
                f"Relation '{triple['relation']}' is not defined")
        # Concept must be defined
        concept_defined = triple['concept'] in json['concepts'] or triple['concept'] in json['individuals']
        if not concept_defined:
            raise Exception(
                f"Concept '{triple['concept']}' is not defined")


def complete_json(result):
    import json
    return json.dumps(result, indent=2)


def complete_owl(json):
    validate_json(json)

    output = ''
    output += '<?xml version="1.0" encoding="UTF-8"?>\n'
    output += '\n'
    output += '<Ontology\n'
    output += '  xmlns="http://www.w3.org/2002/07/owl#"\n'
    output += '  xml:base="http://www.semanticweb.org/gepl/ontologies/2020/10/w_16813858554167876_"\n'
    output += '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    output += '  xmlns:xml="http://www.w3.org/XML/1998/namespace"\n'
    output += '  xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n'
    output += '  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n'
    output += '  ontologyIRI="http://www.semanticweb.org/gepl/ontologies/2020/10/w_16813858554167876_"\n'
    output += '>\n'
    output += '  <Prefix name="" IRI="http://www.semanticweb.org/gepl/ontologies/2020/10/w_16813858554167876_"/>\n'
    output += '  <Prefix name="owl" IRI="http://www.w3.org/2002/07/owl#"/>\n'
    output += '  <Prefix name="rdf" IRI="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>\n'
    output += '  <Prefix name="xml" IRI="http://www.w3.org/XML/1998/namespace"/>\n'
    output += '  <Prefix name="xsd" IRI="http://www.w3.org/2001/XMLSchema#"/>\n'
    output += '  <Prefix name="rdfs" IRI="http://www.w3.org/2000/01/rdf-schema#"/>\n'
    output += '\n'
    for individual in json['individuals']:
        output += f'  <Declaration><NamedIndividual IRI="#{individual}"/></Declaration>\n'
    output += '\n'
    for concept in json['concepts']:
        output += f'  <Declaration><Class IRI="#{concept}"/></Declaration>\n'
    output += '\n'
    relations = json['relations'] + ['iof', 'isa']
    for relation in relations:
        output += f'  <Declaration><ObjectProperty IRI="#{relation}"/></Declaration>\n'
    output += '\n'
    for triple in json['triples']:
        if triple['relation'] == 'iof':
            output += f'  <ClassAssertion>\n'
            output += f'    <Class IRI="#{triple["concept"]}"/>\n'
            output += f'    <NamedIndividual IRI="#{triple["individual"]}"/>\n'
            output += f'  </ClassAssertion>\n'
        elif triple['relation'] == 'isa':
            output += f'  <SubClassOf>\n'
            output += f'    <Class IRI="#{triple["individual"]}"/>\n'
            output += f'    <Class IRI="#{triple["concept"]}"/>\n'
            output += f'  </SubClassOf>\n'
        else:
            output += f'  <ObjectPropertyAssertion>\n'
            output += f'    <ObjectProperty IRI="#{triple["relation"]}"/>\n'
            output += f'    <NamedIndividual IRI="#{triple["individual"]}"/>\n'
            output += f'    <NamedIndividual IRI="#{triple["concept"]}"/>\n'
            output += f'  </ObjectPropertyAssertion>\n'
    output += '</Ontology>\n'
    return output


def complete_prolog(json):
    validate_json(json)

    output = ''

    output += 'not(X) :- X, !, no.\n'
    output += 'not(_).\n'

    output += '\n'
    for concept in json['concepts']:
        output += f'concept({concept}).\n'

    output += '\n'
    for concept, attributes in json['concepts'].items():
        for attribute, typ in attributes.items():
            output += f'attribute({concept}, [{attribute}:{typ}]).\n'

    output += '\n'
    relations = json['relations'] + ['iof', 'isa']
    for relation in relations:
        output += f'relation({relation}).\n'

    output += '\n'
    for individual in json['individuals']:
        output += f'individual({individual}).\n'

    last = None
    for triple in sorted(json['triples'], key=lambda x: x['relation']):
        if last != triple['relation']:
            output += f'\n'
            last = triple['relation']
        output += f'{triple["relation"]}({triple["individual"]}, {triple["concept"]}).\n'

    triple_relations = [triple['relation'] for triple in json['triples']]
    for relation in set(relations) - set(triple_relations):
        if last != relation:
            output += f'\n'
            last = relation
        output += f'{relation}(_, _) :- false.\n'

    output += '\n'
    for triple in json['triples']:
        for key, value in triple['properties'].items():
            output += f'property({triple["individual"]}, [{value[0]}]).\n'

    output += '\n'
    output += 'classOf(X, Y) :- iof(X, Y).\n'
    output += 'classOf(X, Y) :- isa(X, Y).\n'

    output += '\n'
    output += 'concepts(X, Y) :- concept(X), classOf(Y, X), !.\n'
    output += "concepts(X, Y) :- write('One of terms '), write(X), write(' or '), write(Y), write(' is not a Concept.'), nl.\n"

    output += '\n'
    output += 'validIsa(X, Y) :- isa(X, Y), concepts(X, Y), fail.\n'
    output += "validIsa(_, _) :- write('End of validation.'), nl.\n"

    output += '\n'
    output += 'individualAndConcept(I, C) :- individual(I), concept(C), !.\n'
    output += "individualAndConcept(I, C) :- write('One of terms '), write(I), write(' or '), write(C), write(' is not an Individual or a Concept.'), nl.\n"

    output += '\n'
    output += 'validIof(I, C) :- iof(I, C), individualAndConcept(I, C), fail.\n'
    output += "validIof(_, _) :- write('End of validation.'), nl.\n"

    return output


def complete_dot(json):
    validate_json(json)

    nodes = set()
    dot = f'digraph {json["ontology"]} {{'

    dot += '\n  // individuals\n'
    for key in sorted(json['individuals']):
        dot += f'  "{key}" [shape=rectangle, style=filled, color=goldenrod];\n'

    dot += '\n  // concepts\n'
    for key in sorted(json['concepts']):
        if key not in nodes:
            nodes.add(key)
            dot += f'  "{key}" [shape=ellipse, style=filled, color=turquoise4];\n'

    dot += '\n  // concepts properties\n'
    for key in json['concepts']:
        for prop in json['concepts'][key]:
            if prop not in nodes:
                nodes.add(prop)
                dot += f'  "{prop}" [shape=rectangle, style=solid, color=turquoise4];\n'

    dot += '\n  // concepts properties relations\n'
    for key in json['concepts']:
        for prop in json['concepts'][key]:
            dot += f'  "{key}" -> "{prop}" [label="Properties", style=dotted, color=red];\n'

    dot += '\n  // triples\n'
    for it in json['triples']:
        dot += f'  "{it["individual"]}" -> "{it["concept"]}" [label="{it["relation"]}", style=solid, color=black];\n'

    dot += '\n  // triples attributes & relations\n'
    for it in json['triples']:
        for attr in it['properties']:
            value = it['properties'][attr][0].replace('"', "'")
            node = f'"{attr}={value}"'
            dot += f'  {node} [shape=rectangle,color=goldenrod];\n'
            dot += f'  "{it["individual"]}" -> {node} [label="properties", style=dotted, color=red];\n'

    dot += '}\n'
    return dot


def emit_result(result: str, output=None):
    if output:
        with open(output, 'w') as f:
            f.write(result + '\n')
    else:
        print(result)


def create_parser(*args, **kwargs):
    from lark import Lark
    return Lark(grammar, parser='lalr', *args, **kwargs)


def complete_json_with(content: str, complete, output=None):
    parser = create_parser(transformer=JsonTransformer())
    emit_result(complete(parser.parse(content)), output)


def parse_args():
    import argparse
    argparser = argparse.ArgumentParser(description='ONTODL language parser')
    argparser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*',
                           help='ONTODL file', default=[])
    argparser.add_argument('-f', '--format', type=str, default='dot',
                           choices=['dot', 'prolog', 'owl',
                                    'json', 'log', 'tree'],
                           help='Output format')
    argparser.add_argument('-g', '--grammar', action='store_true',
                           help='Show grammar', default=False)
    argparser.add_argument('-o', '--output', type=str, help='Output file')
    args = argparser.parse_args()
    if not args.files and not args.grammar:
        argparser.error('the following arguments are required: files')
    return args


def execute(show_grammar: bool, file=None, format='dot', output=None):
    if show_grammar:
        emit_result(grammar.strip(), output)
    elif format == 'dot':
        complete_json_with(file.read(), complete_dot, output)
    elif format == 'json':
        complete_json_with(file.read(), complete_json, output)
    elif format == 'prolog':
        complete_json_with(file.read(), complete_prolog, output)
    elif format == 'owl':
        complete_json_with(file.read(), complete_owl, output)
    elif format == 'log':
        from lark import Lark
        parser = Lark(grammar)
        emit_result(parser.parse(file.read()).pretty(), output)
    elif format == 'tree':
        from lark import Lark, tree
        parser = Lark(grammar)
        print(tree.pydot__tree_to_graph(parser.parse(file.read())))
    else:
        raise ValueError('Invalid format: ' + format)


if __name__ == '__main__':
    args = parse_args()
    if args.files:
        for file in args.files:
            execute(args.grammar, file, args.format, args.output)
    elif args.grammar:
        execute(args.grammar, None, args.format, args.output)
