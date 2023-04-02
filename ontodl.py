'''
# ONTODL Language Specification

This is the specification for the ONTODL language. ONTODL is a language for describing ontologies.

# The ONTODL Syntax

The syntax of ONTODL is:

```
root            : ontology concepts individuals relations triples '.'
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
    '''root : ontology concepts individuals relations triples '.' '''
    p.parser.accept('root', p)

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
        pass

    def validate_json(json):
        if 'ontology' not in json:
            raise Exception("Missing ontology")
        if 'concepts' not in json:
            raise Exception("Missing concepts")
        if 'individuals' not in json:
            raise Exception("Missing individuals")
        if 'relations' not in json:
            raise Exception("Missing relations")
        if 'triples' not in json:
            raise Exception("Missing triples")

        builtin_relations = ['isa', 'iof']
        for relation in json['relations']:
            if relation in builtin_relations:
                raise Exception(f"Relation '{relation}' is a builtin relation")

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
                concept = json['concepts'][triple['concept']]
                # Properties must be defined
                for prop, typ in triple['properties'].items():
                    typ = typ[1]
                    if prop not in concept:
                        raise Exception(
                            f"Property '{prop}' is not defined in concept '{triple['concept']}'")
                    if typ != concept[prop]:
                        raise Exception(
                            f"Property '{prop}' is of type '{concept[prop]}' in concept '{triple['concept']}', but is of type '{typ}' in triple")
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
            else:
                p[0] = []
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

    def complete_json():
        return parser.result

    def complete_dot():
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
        parser.result = {}
    elif out == 'log':
        parser.accept = accept_log
        parser.complete = complete_log
    elif out == 'dot':
        parser.accept = accept_json
        parser.complete = complete_dot
    else:
        raise Exception(f'Unknown output type: {out} ["json", "log"]')

    return parser


def parse_args():
    import argparse
    argparser = argparse.ArgumentParser(description='ONTODL language parser')
    argparser.add_argument('file', type=argparse.FileType('r'))
    argparser.add_argument('--tokenize', action='store_true',
                           help='Tokenize only')
    argparser.add_argument('-f', '--format', type=str, default='dot',
                           choices=['dot', 'log', 'json'],
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
    if format == 'json':
        import json
        output.write(json.dumps(parser.result, indent=2))
    else:
        output.write(str(parser.complete()))


if __name__ == '__main__':
    args = parse_args()
    execute(args.file, args.tokenize, args.format, args.output)
