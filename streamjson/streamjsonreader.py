import json
from json import JSONDecodeError
from typing import Any


class StreamJSONReader:
    def __init__(self, file: str, encoding: str = 'utf8', **kwds: Any):
        """
        Read objects from a JSON file using a stream. Does not require loading the whole JSON file in memory.

        :param file: The file
        :param encoding: Determines the encoding
        :param kwds: Arguments for json.loads()
        """

        self.__file = file
        self.__encoding = encoding
        self.__kwds = kwds

    def __enter__(self):
        self.__reader = self.Reader(file=self.__file, encoding=self.__encoding, **self.__kwds)
        return self.__reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__reader.close()

    class Reader:
        def __init__(self, file: str, encoding: str = 'utf8', **kwds: Any):
            """
            :param file: The file
            :param encoding: Determines the encoding
            :param kwds: Arguments for json.loads()
            """

            self.__file = file
            self.__encoding = encoding
            self.__kwds = kwds

            self.__opened_file = None
            self.__tmp_lines = ''
            self.__object_is_pending = False
            self.__opening_bracket_index = 0
            self.__size_bytes = 0

        def find(self):
            """ Find JSON object """

            # Open the file
            self.__opened_file = open(self.__file, 'r', encoding=self.__encoding)

            # Loop through each line in the JSON file and while doing so, yield JSON objects as they are found
            for line in self.__opened_file:
                # Append new line to tmp_lines
                new_line = ''.join(line.splitlines())
                self.__tmp_lines += new_line

                # FIND OPENING BRACKET {

                # Not object_is_pending means there is no opening bracket expecting a closing bracket at the moment
                # Therefore it is necessary to look for the opening bracket
                if not self.__object_is_pending:
                    # Find the opening bracket and its index
                    self.__opening_bracket_index = self.__tmp_lines.find('{', 0)
                    # If nothing was found: Clear tmp_lines and continue to try again with the next line from the file
                    if self.__opening_bracket_index == -1:
                        self.__tmp_lines = ''
                        continue
                    else:
                        # If the opening bracket was found:
                        # Set object_is_pending to true meaning a closing bracket is expected next to yield an object
                        self.__object_is_pending = True

                # FIND CLOSING BRACKET }

                # Get all indices of closing brackets in the string
                closing_brackets_indices = [i for i, char in enumerate(self.__tmp_lines) if char == '}']

                # Try all closing brackets for possible JSON object completion
                for closing_bracket_index in closing_brackets_indices:
                    str_possible_json_object = self.__tmp_lines[self.__opening_bracket_index:closing_bracket_index + 1]
                    try:
                        # Try to load the string as a JSON object
                        json_obj = json.loads(s=str_possible_json_object, **self.__kwds)

                        # Clear part of tmp_lines that was used in the object
                        self.__tmp_lines = self.__tmp_lines[closing_bracket_index + 1:]

                        # Set False to start looking for opening bracket next
                        self.__object_is_pending = False

                        # Yield the JSON object
                        yield json_obj

                        # Append the size of the object
                        self.__size_bytes += len(str_possible_json_object.encode('utf-8'))

                        break
                    except JSONDecodeError:
                        continue

        def get_size(self):
            """ Get size of total strings successfully converted to JSON objects from file in bytes """

            return self.__size_bytes

        def close(self):
            """ Close the reader """

            # Close the file
            if self.__opened_file:
                self.__opened_file.close()
