import os
import json


class StreamJSONWriter:
    def __init__(self, name: str, indent: int = 2, ensure_ascii: bool = True):
        """
        Send objects or arrays to a JSON file using a stream. Useful for when you don't want to read large amounts of
        data in memory, for example when you need to save large amounts of data from a database to a single JSON file.

        :param name: The file
        :param indent: Spaces to use at the beginning of line
        :param ensure_ascii: ascii-only json output (replace non-ascii to \ uNNNN), True by default
        """

        self.__name = name
        self.__indent = indent if indent >= 0 else 0
        self.__ensure_ascii = ensure_ascii

    def __enter__(self):
        self.__writer = self.Writer(self.__name, self.__indent, self.__ensure_ascii)
        return self.__writer

    def send(self, value):
        """
        Send value to file

        :param value: The value to send to the file
        """

        self.__writer.send(value)

    def close(self):
        """ Close the writer """

        self.__writer.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__writer.close()

    class Writer:
        def __init__(self, file: str, indent: int, ensure_ascii: bool):
            self.__file = file
            self.__indent = indent
            self.__stream_started = False
            self.__opened_file = None
            self.__ensure_ascii = ensure_ascii

        def send(self, value):
            """
            Send value to file

            :param value: The value to send to the file
            """

            self.__send(value)

        def __send(self, value):
            """
            Send value to file

            :param value: The value to send to the file
            """

            if not self.__stream_started:
                self.__stream_started = True

                # Remove the file before writing to it
                if os.path.exists(self.__file):
                    os.remove(self.__file)

                # Open the file
                self.__opened_file = open(self.__file, 'a')

                # Add opening bracket at first write
                self.__opened_file.write('[')

            # Create JSON string from value
            json_value = json.dumps(
                json.loads(
                    json.dumps(value, ensure_ascii=self.__ensure_ascii)
                ),
                indent=self.__indent,
                ensure_ascii=self.__ensure_ascii
            )

            # Indent the whole value
            json_value_indented = self.__indent_string(json_value)

            self.__opened_file.write(f'\n{json_value_indented},')

        def __indent_string(self, string) -> str:
            """
            Indent a string

            :param string: String to indent
            :return: The indented string
            """

            def get_indent() -> str:
                """ String representing the indentation """

                indent_string = ''
                for x in range(self.__indent):
                    indent_string += ' '
                return indent_string

            indent = get_indent()
            return indent + string.replace('\n', '\n' + indent)

        def __remove_last_comma(self, file):
            """
            Remove the last comma from the file

            :param file: The file
            """

            file.seek(file.tell() - 1, os.SEEK_SET)
            file.truncate()

        def close(self):
            """ Close the writer """

            if self.__stream_started and self.__opened_file:
                # Remove last comma
                self.__remove_last_comma(self.__opened_file)

                # Add the closing bracket
                self.__opened_file.write('\n]')

                # Close the file
                self.__opened_file.close()
