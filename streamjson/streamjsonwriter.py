import os
import json

from .exceptions import StreamJSONError


class StreamJSONWriter:
    def __init__(self, name: str, indent: int = 2):
        """
        Send objects or arrays to a JSON file using a stream. Useful for when you don't want to read large amounts of
        data in memory, for example when you need to save large amounts of data from a database to a single JSON file.

        :param name: The file name
        :param indent: Spaces to use at beginning of line
        """

        if name == '':
            raise StreamJSONError('No file name provided.')
        if indent < 0:
            raise StreamJSONError('Indent cannot be lower than 0.')

        self.__name = name
        self.__indent = indent

    def __enter__(self):
        self.__writer = self.Writer(self.__name, self.__indent)
        return self.__writer

    def send(self, value):
        """
        Call the writer and send the value to write

        :param value: The value to send to the writer
        """

        self.__writer.send(value)

    def close(self):
        """ Call the writer and close the file """

        self.__writer.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__writer.close()

    class Writer:
        def __init__(self, name: str, indent: int):
            self.__name = name
            self.__indent = indent
            self.__stream_started = False
            self.__file = None

        def send(self, value):
            """
            Send value to file
            Value can be a dictionary or a list containing dictionaries

            :param value: The value to write to file
            """

            self.__send(value)

        def __send(self, value):
            """
            Send value to file

            :param value: The value to write to file
            """

            if not self.__stream_started:
                # Remove the file before writing to it
                if os.path.exists(self.__name):
                    os.remove(self.__name)

                # Open the file
                self.__file = open(self.__name, 'a')

                # Add opening bracket at first write
                self.__file.write(f'[')

                self.__stream_started = True

            json_value = json.dumps(json.loads(json.dumps(value)), indent=self.__indent)
            json_value_indented = self.__indent_string(json_value)
            self.__file.write(f'\n{json_value_indented},')

        def close(self):
            """ Close the writer """

            if self.__stream_started:
                # Remove last comma
                self.__remove_last_comma(self.__file)

                # Add the closing bracket
                self.__file.write('\n]')

                # Close the file
                self.__file.close()

        def __indent_string(self, value) -> str:
            """
            Indent a string

            :param value: String to indent
            :return: The indented string
            """

            def get_indent() -> str:
                """ String representing the indentation """

                indent_string = ''
                for x in range(self.__indent):
                    indent_string += ' '
                return indent_string

            indent = get_indent()
            return indent + value.replace('\n', '\n' + indent)

        def __remove_last_comma(self, file):
            """
            Remove the last comma from the file

            :param file: The file
            """

            file.seek(file.tell() - 1, os.SEEK_SET)
            file.truncate()
