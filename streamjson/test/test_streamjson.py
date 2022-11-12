import os
import json

import pytest

from streamjson import StreamJSONWriter, StreamJSONReader

test_json_file = os.path.join(os.path.dirname(__file__), 'test.json')


class TestStreamJSON:
    def test_writer_send(self):
        """ Test the writer """

        persons = [
            {'id': '0001', 'first_name': 'John', 'last_name': 'Doe'},
            {'id': '0002', 'first_name': 'Jane', 'last_name': 'Doe'}
        ]

        with StreamJSONWriter(test_json_file, indent=2) as writer:
            for person in persons:
                writer.send(person)

        with open(test_json_file, 'r') as opened_file:
            expected = persons
            result = json.load(opened_file)
            assert expected == result

    def test_reader_find(self):
        """ Test the reader """

        persons_json_file = os.path.join(os.path.dirname(__file__), 'persons.json')
        with StreamJSONReader(persons_json_file) as reader:
            reader_generator = reader.find()
            obj_1 = next(reader_generator)
            assert obj_1 == {'id': '0001',
                             'first_name': 'John',
                             'last_name': 'Doe',
                             "hobbies": [{"name": "photography"}, {"name": "programming"}, {"name": "hiking"}]
                             }
            obj_2 = next(reader_generator)
            assert obj_2 == {'id': '0002',
                             'first_name': 'Jane',
                             'last_name': 'Doe',
                             "hobbies": [{"name": "dancing"}]
                             }

    @pytest.fixture(scope='session', autouse=True)
    def cleanup(self):
        """ Delete test file after all tests are finished """

        yield
        if os.path.exists(test_json_file):
            os.remove(test_json_file)
