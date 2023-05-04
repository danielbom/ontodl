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
