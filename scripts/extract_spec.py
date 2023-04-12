import os
import sys

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_path)


def extract_spec():
    import ontodl

    newline_before = ['ontology', 'concepts', 'individuals',
                      'relations', 'triples', 'value']
    funcs = [getattr(ontodl, k) for k in dir(ontodl) if k.startswith('p_')]
    funcs.sort(key=lambda f: f.__code__.co_firstlineno)
    funcs_docs = [f.__doc__ for f in funcs if f.__doc__]

    specs = []
    for doc in funcs_docs:
        lines = doc.splitlines()
        result = []
        for line in lines:
            line = line.strip()
            if line == '|':
                line = '| <empty>'
            result.append(line)
        result = ' '.join(result)
        [rule, body] = result.split(':', 1)
        rule = rule.strip()
        body = body.strip()
        specs.append((rule, body))

    biggest_rule = max([len(rule) for rule, _ in specs])

    for rule, body in specs:
        body = body.split(' | ')
        if rule in newline_before:
            print()
        print(f'{rule.ljust(biggest_rule)} : {body[0]}')
        for it in body[1:]:
            print(f'{"":{biggest_rule}} | {it}')


extract_spec()
