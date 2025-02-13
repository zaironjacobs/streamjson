import os
import json

import pytest

from streamjson import StreamJSONWriter, StreamJSONReader

tmp_json_file = os.path.join(os.path.dirname(__file__), "test.json")


class TestStreamJSON:
    def test_writer_send(self):
        persons = [
            {"id": "0001", "first_name": "John", "last_name": "Doe"},
            {"id": "0002", "first_name": "Jane", "last_name": "Doe"},
        ]

        with StreamJSONWriter(tmp_json_file, indent=2) as writer:
            for person in persons:
                writer.send(person)

        with open(tmp_json_file, "r") as file:
            expected = persons
            result = json.load(file)

            assert expected == result

    def test_reader_find(self):
        persons_json_file = os.path.join(os.path.dirname(__file__), "persons.json")
        with StreamJSONReader(persons_json_file) as reader:
            reader_generator = reader.find()
            obj_1 = next(reader_generator)
            obj_2 = next(reader_generator)

            assert obj_1 == {
                "id": "0001",
                "first_name": "John",
                "last_name": "Doe",
                "hobbies": [
                    {"name": "photography"},
                    {"name": "programming"},
                    {"name": "hiking"},
                ],
            } and obj_2 == {
                "id": "0002",
                "first_name": "Jane",
                "last_name": "Doe",
                "hobbies": [{"name": "dancing"}],
            }

    @pytest.fixture(scope="session", autouse=True)
    def cleanup(self):
        """
        Delete file after tests are finished.
        """

        yield
        if os.path.exists(tmp_json_file):
            os.remove(tmp_json_file)
