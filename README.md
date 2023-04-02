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
