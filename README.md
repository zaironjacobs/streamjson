StreamJSON
=================
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/streamjson?color=blue)](https://pypi.python.org/pypi/streamjson)
[![PyPI](https://img.shields.io/pypi/v/streamjson?color=blue)](https://pypi.python.org/pypi/streamjson)
[![PyPI - Status](https://img.shields.io/pypi/status/streamjson)](https://pypi.python.org/pypi/streamjson)
[![PyPI - License](https://img.shields.io/pypi/l/streamjson)](https://pypi.python.org/pypi/streamjson)

Send objects or arrays to a JSON file using a stream. Useful for when you don't want to read large amounts of data in
memory, for example when you need to save large amounts of data from a database to a single JSON file.

## Install

To install:

```console
$ pip install streamjson
```

To upgrade:

```console
$ pip install streamjson --upgrade
```

#### Usage

Fetch data from a database or anywhere else and send to a JSON file. The send function takes in a dictionary or a list.
A new file with the given name will be created, the root of the JSON file is an array by default.

```Python
from streamjson import StreamJSONWriter

persons = [{'id': '0001', 'first_name': 'John', 'last_name': 'Doe'},
           {'id': '0002', 'first_name': 'Jane', 'last_name': 'Doe'}]

with StreamJSONWriter('persons.json', indent=2) as writer:
    for person in persons:
        writer.send(person)
```

persons.json:

```JSON
[
  {
    "id": "0001",
    "first_name": "John",
    "last_name": "Doe"
  },
  {
    "id": "0002",
    "first_name": "Jane",
    "last_name": "Doe"
  }
]
```
