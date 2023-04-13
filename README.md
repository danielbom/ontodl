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
python3 ontodl.py samples/ontodl_sample2.ontodl --format prolog
python3 ontodl.py samples/ontodl_sample2.ontodl --format owl # Web Ontology Language
python3 ontodl.py samples/ontodl_sample1.ontodl --format json
python3 ontodl.py samples/ontodl_sample2.ontodl --format log
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
