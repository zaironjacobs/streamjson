import os
import json

import pytest

from streamjson import StreamJSONWriter

file = os.path.join(os.path.dirname(__file__), 'test.json')


# README shields & tests
class TestStreamJSONWriter:

    def test_send(self):
        persons = []
        for x in range(100):
            persons.append({'id': x, 'first_name': 'John', 'last_name': 'Doe'})
        for x in range(100, 200):
            persons.append({'id': x, 'first_name': 'Jane', 'last_name': 'Doe'})

        with StreamJSONWriter(file, indent=2) as writer:
            for person in persons:
                writer.send(person)

        with open(file, 'r') as opened_file:
            expected = persons
            result = json.load(opened_file)
            assert expected == result

    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self):
        yield
        if os.path.exists(file):
            os.remove(file)
