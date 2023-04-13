'''
# ONTODL Language Specification

This is the specification for the ONTODL language. ONTODL is a language for describing ontologies.

You can try an online version of ONTODL to DOT [here](https://webontodl.epl.di.uminho.pt/). 

You can find the source code in [Github](https://github.com/danielbom/ontodl).

# Get started

To use this script, you need have ply installed.

```
# create a virtual environment (optional)
python -m venv venv 
source venv/bin/activate    # linux
./venv/Scripts/activate.ps1 # windows powershell

# install ply
pip install ply
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
python3 ontodl.py samples/ontodl_sample2.ontodl --format dot:legacy
python3 ontodl.py samples/ontodl_sample2.ontodl --format prolog
python3 ontodl.py samples/ontodl_sample2.ontodl --format log
python3 ontodl.py samples/ontodl_sample1.ontodl --format json
```

Looks for the tokenization of the input:

```bash
python3 ontodl.py samples/ontodl_sample1.ontodl --tokenize
python3 ontodl.py samples/ontodl_sample2.ontodl --tokenize
```

# The ONTODL Syntax

The syntax of ONTODL is:

```
root            : ontology concepts individuals relations triples end
end             : '.'

ontology        : ONTOLOGY id

concepts        : CONCEPTS '{' concept_list '}'
concept_list    : concept_list ',' concept
                | concept
                | <empty>
concept         : id '[' attribute_list ']'
                | id
attribute_list  : attribute_list ',' attribute
                | attribute
                | <empty>
attribute       : id ':' type

individuals     : INDIVIDUALS '{' individual_list '}'
individual_list : individual_list ',' individual
                | individual
                | <empty>
individual      : id

relations       : RELATIONS '{' relation_list '}'
relation_list   : relation_list ',' relation
                | relation
                | <empty>
relation        : id

triples         : TRIPLES '{' triple_list '}'
triple_list     : triple_list triple
                | triple
                | <empty>
triple          : id '=' id IMPLIES entity ';'
entity          : id '[' properties_list ']'
                | id
properties_list : properties_list ',' property
                | property
                | <empty>
property        : id '=' value

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
```

- ID allows accents.
- BOOLEAN accepts true, false.
- STRING accepts double-quoted strings.
- NUMBER accepts integers, floats, and scientific notation.
- DATE accepts date, datetime (with T or space separation), and ISO 8601 date format
- ONTOLOGY, CONCEPTS, INDIVIDUALS, RELATIONS, and TRIPLES allows english or portuguese literals.
'''

import sys

tokens = ('ONTOLOGY', 'CONCEPTS', 'INDIVIDUALS', 'RELATIONS', 'TRIPLES',
          'TYPES', 'ID', 'NUMBER', 'BOOLEAN', 'STRING', 'DATE', 'IMPLIES')
literals = ('{', '}', '[', ']', ':', ';', ',', '.', '=')


def t_ONTOLOGY(t):
    r'(Ontologia|Ontology)'
    return t


def t_CONCEPTS(t):
    r'(conceitos|concepts)'
    return t


def t_INDIVIDUALS(t):
    r'(individuos|individuals)'
    return t


def t_RELATIONS(t):
    r'(relacoes|relations)'
    return t


def t_TRIPLES(t):
    r'(triplos|triples)'
    return t


def t_TYPES(t):
    r'(string|integer|float|boolean|date)'
    return t


def t_BOOLEAN(t):
    r'(true|false)'
    return t


def t_ID(t):
    r'[a-zA-ZÀ-ÖØ-öø-ÿ_][a-zA-ZÀ-ÖØ-öø-ÿ0-9_]*'
    # accept accented characters
    return t


def t_DATE(t):
    r'\d{4}-\d{2}-\d{2}([T ](\d{2}:\d{2}:\d{2}(\.\d+)?(\.0+)?)(Z|(\+|-)\d{2}:\d{2})?)?'
    # accept date, datetime (w/ T or space separation), and ISO 8601 date format
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?([eE][+-]?\d+)?'
    # accept integer, float, and scientific notation
    return t


def t_STRING(t):
    r'\"[^"]*\"'
    return t


def t_IMPLIES(t):
    r'=>'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ' \t\r\n'


def create_lexer():
    from ply.lex import lex
    return lex()

# Root


def p_root(p):
    '''root : ontology concepts individuals relations triples end '''
    p.parser.accept('root', p)


def p_end(p):
    '''end : '.' '''
    p.parser.accept('end', p)

# Ontology


def p_ontology(p):
    '''ontology : ONTOLOGY id '''
    p.parser.accept('ontology', p)

# Concepts


def p_concepts(p):
    '''concepts : CONCEPTS '{' concept_list '}' '''
    p.parser.accept('concepts', p)


def p_concept_list(p):
    '''concept_list : concept_list ',' concept
                    | concept
                    |'''
    p.parser.accept('concept_list', p)


def p_concept(p):
    '''concept : id '[' attribute_list ']'
                | id
    '''
    p.parser.accept('concept', p)


def p_attribute_list(p):
    '''attribute_list : attribute_list ',' attribute
                      | attribute
                      |'''
    p.parser.accept('attribute_list', p)


def p_attribute(p):
    '''attribute : id ':' type'''
    p.parser.accept('attribute', p)

# Individuals


def p_individuals(p):
    '''individuals : INDIVIDUALS '{' individual_list '}' '''
    p.parser.accept('individuals', p)


def p_individual_list(p):
    '''individual_list : individual_list ',' individual
                       | individual
                       |'''
    p.parser.accept('individual_list', p)


def p_individual(p):
    '''individual : id'''
    p.parser.accept('individual', p)

# Relations


def p_relations(p):
    '''relations : RELATIONS '{' relation_list '}' '''
    p.parser.accept('relations', p)


def p_relation_list(p):
    '''relation_list : relation_list ',' relation
                     | relation
                     |'''
    p.parser.accept('relation_list', p)


def p_relation(p):
    '''relation : id'''
    p.parser.accept('relation', p)

# Triples


def p_triples(p):
    '''triples : TRIPLES '{' triple_list '}' '''
    p.parser.accept('triples', p)


def p_triple_list(p):
    '''triple_list : triple_list triple
                   | triple
                   |'''
    p.parser.accept('triple_list', p)


def p_triple(p):
    '''triple : id '=' id IMPLIES entity ';' '''
    p.parser.accept('triple', p)


def p_entity(p):
    '''entity : id '[' properties_list ']'
              | id
    '''
    p.parser.accept('entity', p)


def p_properties_list(p):
    '''properties_list : properties_list ',' property
                       | property
                       |'''
    p.parser.accept('properties_list', p)


def p_property(p):
    '''property : id '=' value'''
    p.parser.accept('property', p)


def p_value(p):
    '''value : number
             | boolean
             | string
             | date
    '''
    p.parser.accept('value', p)

# Atoms


def p_number(p):
    '''number : NUMBER'''
    p.parser.accept('number', p)


def p_boolean(p):
    '''boolean : BOOLEAN'''
    p.parser.accept('boolean', p)


def p_string(p):
    '''string : STRING'''
    p.parser.accept('string', p)


def p_date(p):
    '''date : DATE'''
    p.parser.accept('date', p)


def p_type(p):
    '''type : TYPES'''
    p.parser.accept('type', p)


def p_id(p):
    '''id : ID
        | STRING'''
    p.parser.accept('id', p)


def p_error(p):
    if p:
        raise Exception(f"Syntax error at '{p}'")
    else:
        raise Exception("Syntax error at EOF")


def create_parser(out='log'):
    def accept_log(name, p):
        p[0] = p[1:]
        print(name, p[0])

    def complete_log():
        return ""

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
            # Individual must be defined
            if triple['individual'] not in json['individuals']:
                raise Exception(
                    f"Individual '{triple['individual']}' is not defined")
            # Relation must be defined
            if triple['relation'] not in all_relations:
                raise Exception(
                    f"Relation '{triple['relation']}' is not defined")
            # Concept must be defined
            concept_defined = False
            if triple['concept'] in json['concepts']:
                concept_defined = True
                concept_name = triple['concept']
                concept = json['concepts'][concept_name]
                properties = triple['properties']
                # Properties must be defined in concept
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

            if triple['concept'] in json['individuals']:
                concept_defined = True
            if not concept_defined:
                raise Exception(
                    f"Concept '{triple['concept']}' is not defined")

    def accept_json(name, p):
        if name == 'root':
            p.parser.result = {
                'ontology': p[1],
                'concepts': p[2],
                'individuals': p[3],
                'relations': p[4],
                'triples': p[5]
            }
        elif name == 'end':
            pass
        # Ontology
        elif name == 'ontology':
            p[0] = p[2]
        # Concepts
        elif name == 'concepts':
            p[0] = dict(p[3])
        elif name == 'concept_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'concept':
            if len(p) == 5:
                p[0] = [p[1], dict(p[3])]
            elif len(p) == 2:
                p[0] = [p[1], {}]
        elif name == 'attribute_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'attribute':
            p[0] = [p[1], p[3]]
        # Individuals
        elif name == 'individuals':
            p[0] = p[3]
        elif name == 'individual_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'individual':
            p[0] = p[1]
        # Relations
        elif name == 'relations':
            p[0] = p[3]
        elif name == 'relation_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'relation':
            p[0] = p[1]
        # Triples
        elif name == 'triples':
            p[0] = p[3]
        elif name == 'triple_list':
            if len(p) == 3:
                p[0] = p[1] + [p[2]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'triple':
            p[0] = {
                'individual': p[1],
                'relation': p[3],
                'concept': p[5]['concept'],
                'properties': p[5]['properties'],
            }
        elif name == 'entity':
            if len(p) == 5:
                p[0] = {"concept": p[1], "properties": dict(p[3])}
            elif len(p) == 2:
                p[0] = {"concept": p[1], "properties": {}}
        elif name == 'properties_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'property':
            p[0] = [p[1], p[3]]
        elif name == 'value':
            p[0] = p[1]
        # Atoms
        elif name == 'number':
            p[0] = [p[1], name]
        elif name == 'boolean':
            p[0] = [p[1], name]
        elif name == 'string':
            p[0] = [p[1], name]
        elif name == 'date':
            p[0] = [p[1], name]
        elif name == 'type':
            p[0] = p[1]
        elif name == 'id':
            p[0] = p[1].strip('"')
        else:
            print(f'Unknown name: {name}')

    def accept_dot(name, p):
        if name == 'root':
            pass
        elif name == 'end':
            p.parser.result['output'].append('}\n')
        # Ontology
        elif name == 'ontology':
            p.parser.result['output'].append(f'digraph {p[2]} {{')
        # Concepts
        elif name == 'concepts':
            pass
        elif name == 'concept_list':
            pass
        elif name == 'concept':
            concept = p[1]
            if concept in p.parser.result['entries']:
                raise Exception(
                    f'Entry with name "{concept}" already exists as {p.parser.result["entries"][concept]["type"]}')
            if len(p) == 5:
                attributes = dict(p[3])
            elif len(p) == 2:
                attributes = {}
            p.parser.result['entries'][concept] = {
                'type': 'concept',
                'attributes': attributes
            }
            p.parser.result['output'].append(
                f'  "{concept}" [label="{concept}", shape=ellipse, style=filled, color=turquoise4];')
            for attribute, value in attributes.items():
                p.parser.result['output'].append(
                    f'  "{attribute}" [shape=rectangle, color=turquoise4];')
                p.parser.result['output'].append(
                    f'  "{concept}" -> "{attribute}" [label="Properties", style=dotted, color=red];')
        elif name == 'attribute_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'attribute':
            p[0] = [p[1], p[3]]
        # Individuals
        elif name == 'individuals':
            pass
        elif name == 'individual_list':
            pass
        elif name == 'individual':
            individual = p[1]
            if individual in p.parser.result['entries']:
                raise Exception(
                    f'Entry with name "{individual}" already exists as {p.parser.result["entries"][individual]["type"]}.')
            p.parser.result['entries'][individual] = {'type': 'individual'}
            p.parser.result['output'].append(
                f'  "{individual}" [shape=rectangle, style=filled, color=goldenrod];')
        # Relations
        elif name == 'relations':
            pass
        elif name == 'relation_list':
            pass
        elif name == 'relation':
            relation = p[1]
            if relation in p.parser.result['entries']:
                raise Exception(
                    f'Entry with name "{relation}" already exists as {p.parser.result["entries"][relation]["type"]}.')
            p.parser.result['entries'][relation] = {'type': 'relation'}
        # Triples
        elif name == 'triples':
            pass
        elif name == 'triple_list':
            pass
        elif name == 'triple':
            individual = p[1]
            relation = p[3]
            concept = p[5]['concept']
            properties = p[5]['properties']

            if individual not in p.parser.result['entries']:
                raise Exception(f'Individual "{individual}" does not exist.')
            if relation not in p.parser.result['entries']:
                raise Exception(f'Relation "{relation}" does not exist.')
            if concept not in p.parser.result['entries']:
                raise Exception(f'Concept "{concept}" does not exist.')

            if p.parser.result['entries'][individual]['type'] != 'individual':
                raise Exception(f'Entry "{individual}" is not an individual.')
            if p.parser.result['entries'][relation]['type'] != 'relation':
                raise Exception(f'Entry "{relation}" is not a relation.')
            if p.parser.result['entries'][concept]['type'] not in ['concept', 'individual']:
                raise Exception(
                    f'Entry "{concept}" is not a concept or an individual.')

            entry_concept = p.parser.result['entries'][concept]
            if entry_concept['type'] == 'concept':
                for key, value in properties.items():
                    if key not in entry_concept['attributes']:
                        raise Exception(
                            f'Concept "{concept}" does not have attribute "{key}".')
                    if entry_concept['attributes'][key] != value[1]:
                        raise Exception(
                            f'Attribute "{key}" of concept "{concept}" is of type "{entry_concept["attributes"][key]}", not "{value[1]}".')
                for key, value in entry_concept['attributes'].items():
                    if key not in properties:
                        raise Exception(
                            f'Attribute "{key}" of concept "{concept}" is not set.')

            p.parser.result['output'].append(
                f'  "{individual}" -> "{concept}" [label="{relation}", style=solid, color=black];')

            for key, value in properties.items():
                node = f'{key}={value[0]}'.replace('"', "'")
                p.parser.result['output'].append(
                    f'  "{node}" [shape=rectangle, color=goldenrod];')
                p.parser.result['output'].append(
                    f'  "{individual}" -> "{node}" [label="properties", style=dotted, color=red];')
        elif name == 'entity':
            if len(p) == 5:
                p[0] = {"concept": p[1], "properties": dict(p[3])}
            elif len(p) == 2:
                p[0] = {"concept": p[1], "properties": {}}
        elif name == 'properties_list':
            if len(p) == 4:
                p[0] = p[1] + [p[3]]
            elif len(p) == 2:
                p[0] = [p[1]]
            else:
                p[0] = []
        elif name == 'property':
            p[0] = [p[1], p[3]]
        elif name == 'value':
            p[0] = p[1]
        # Atoms
        elif name == 'number':
            p[0] = [p[1], name]
        elif name == 'boolean':
            p[0] = [p[1], name]
        elif name == 'string':
            p[0] = [p[1], name]
        elif name == 'date':
            p[0] = [p[1], name]
        elif name == 'type':
            p[0] = p[1]
        elif name == 'id':
            p[0] = p[1].strip('"')
        else:
            print(f'Unknown name: {name}')

    def complete_dot():
        return '\n'.join(parser.result['output'])

    def complete_json():
        import json
        return json.dumps(parser.result, indent=2)

    def complete_prolog():
        json = parser.result
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

    def complete_dot_legacy():
        json = parser.result
        validate_json(json)

        nodes = set()
        dot = f'digraph {json["ontology"]} {{'

        dot += '\n  // individuals\n'
        dot += '  node [shape=rectangle, style=filled, color=goldenrod];\n'
        for key in sorted(json['individuals']):
            dot += f'  "{key}";\n'

        dot += '\n  // concepts\n'
        dot += '  node [shape=ellipse, style=filled, color=turquoise4];\n'
        for key in sorted(json['concepts']):
            if key not in nodes:
                nodes.add(key)
                dot += f'  "{key}";\n'

        dot += '\n  // concepts properties\n'
        dot += '  node [shape=rectangle, style=solid, color=turquoise4];\n'
        for key in json['concepts']:
            for prop in json['concepts'][key]:
                if prop not in nodes:
                    nodes.add(prop)
                    dot += f'  "{prop}";\n'

        dot += '\n  // concepts properties relations\n'
        dot += '  edge [label="Properties", style=dotted, color=red];\n'
        for key in json['concepts']:
            for prop in json['concepts'][key]:
                dot += f'  "{key}" -> "{prop}";\n'

        dot += '\n  // triples\n'
        dot += '  edge [style=solid, color=black];\n'
        for it in json['triples']:
            dot += f'  "{it["individual"]}" -> "{it["concept"]}" [label="{it["relation"]}"];\n'

        dot += '\n  // triples attributes & relations\n'
        dot += '  node [shape=rectangle,color=goldenrod];\n'
        dot += '  edge [label="properties", style=dotted, color=red];\n'
        for it in json['triples']:
            for attr in it['properties']:
                value = it['properties'][attr][0].replace('"', "'")
                node = f'"{attr}={value}"'
                dot += f'  {node};\n'
                dot += f'  "{it["individual"]}" -> {node};\n'

        dot += '}\n'
        return dot

    from ply.yacc import yacc
    parser = yacc()

    if out == 'json':
        parser.accept = accept_json
        parser.complete = complete_json
    elif out == 'log':
        parser.accept = accept_log
        parser.complete = complete_log
    elif out == 'dot:legacy':
        parser.accept = accept_json
        parser.complete = complete_dot_legacy
    elif out == 'dot':
        parser.accept = accept_dot
        parser.complete = complete_dot
        parser.result = {
            'entries': {
                'iof': {'type': 'relation'},
                'isa': {'type': 'relation'},
            },
            'output': []
        }
    elif out == 'prolog':
        parser.accept = accept_json
        parser.complete = complete_prolog
    else:
        raise Exception(
            f'Unknown output type: {out} ["json", "log", "dot", "dot:legacy"]')

    return parser


def parse_args():
    import argparse
    argparser = argparse.ArgumentParser(description='ONTODL language parser')
    argparser.add_argument('file', type=argparse.FileType('r'))
    argparser.add_argument('--tokenize', action='store_true',
                           help='Tokenize only')
    argparser.add_argument('-f', '--format', type=str, default='dot',
                           choices=['dot', 'dot:legacy',
                                    'log', 'json', 'prolog'],
                           help='Output format')
    argparser.add_argument('-o', '--output', type=argparse.FileType('w'),
                           default=sys.stdout,
                           help='Output file')
    return argparser.parse_args()


def execute(file, tokenize=False, format='dot', output=sys.stdout):
    if tokenize:
        lexer = create_lexer()
        for tok in lexer.tokenize(file.read()):
            print(tok)
        exit(0)

    lexer = create_lexer()
    parser = create_parser(format)
    parser.parse(file.read())
    output.write(parser.complete())


if __name__ == '__main__':
    args = parse_args()
    execute(args.file, args.tokenize, args.format, args.output)
