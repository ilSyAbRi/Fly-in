# from zone import Zone
from rich import print


class CustomParserError(Exception):
    """
    class for custom error
    """
    pass


class StandardParserError(Exception):
    """
    class for standar error
    """
    pass


class LineCleaner:
    """
    helper methodes for parser to clean lines
    """

    def __init__(self, lines_to_clean: list[str]) -> None:
        """
        just set lines to clean to self.data to start cleaning
        """
        self.data = lines_to_clean

    def remove_comments(self) -> "LineCleaner":
        """
        clean lines form comment any comment
        """
        self.data = [line.split("#")[0] for line in self.data]
        return self

    def strip_spaces(self) -> "LineCleaner":
        """
        clean lines from front and up spaces:
        """
        self.data = [line.strip() for line in self.data]
        return self

    def remove_empty_lines(self) -> "LineCleaner":
        """
        skip empty lines just to make good structure to work with
        """
        self.data = [line for line in self.data if line]
        return self


class Parser:
    """
    the main parser class
    """

    def __init__(self, file_path: str) -> None:
        """
        set instance with attribute file_path
        """
        self.file_path = file_path

    def load_raw_input(self) -> list[tuple]:
        """
            Load the map file and preserve original line numbers
            for parser error reporting.
        """
        try:
            with open(self.file_path, 'r') as file:
                content = file.read()

                if not content.strip():
                    raise CustomParserError(f"Empty File: {self.file_path}")

                lines = content.splitlines()
                raw_ln = LineCleaner(lines)
                raw_ln.remove_comments().strip_spaces()
                clean_ln = LineCleaner(lines)
                clean_ln.remove_comments().strip_spaces().remove_empty_lines()
                index_lines = [
                        (i, v)
                        for i, v in enumerate(raw_ln.data, start=1)
                        if v in clean_ln.data
                        ]
                return index_lines

        except OSError as e:
            raise StandardParserError(f"file error -> OSError: {e}")

    def parse_nb_drones(self, clean_indexed_ln: list[tuple]) -> tuple:
        """
            check nb drones if it s valid
            return tuple of key value
        """

        if ":" not in clean_indexed_ln[0][1]:
            raise CustomParserError(f"Line: {clean_indexed_ln[0][0]}\
\nError: <{clean_indexed_ln[0][1]}> you forget :")

        k, v = clean_indexed_ln[0][1].split(":", 1)
        # strip remove : so to return it to the right place i do that
        # to check : in nb_drones if they are a space before it or not
        k = k + ":"
        k = k.strip()
        if k != "nb_drones:":
            raise CustomParserError(f"Line: {clean_indexed_ln[0][0]}\
\nError: '{clean_indexed_ln[0][1]}' first line would be 'nb_drones:'\
 — use exact syntax 'nb_drones:' with no space before ':'")

        if not v:
            raise CustomParserError(f"Line: {clean_indexed_ln[0][0]}\
\nError: enter a number in nb_drones")

        try:
            v = v.strip()
            v = int(v)
            if v <= 0:
                raise CustomParserError(f"Line: {clean_indexed_ln[0][0]}\
\nError: <{v}> should be positive")

        except ValueError:
            raise StandardParserError(f"Line: {clean_indexed_ln[0][0]}\
\nError: <{v}> should be number")

        return (k, v)

    def dispatcher(self) -> None:
        clean_indexed_ln = self.load_raw_input()
        nb_drones_data = self.parse_nb_drones(clean_indexed_ln)
        self.parse_hubs(clean_indexed_ln)
        print(clean_indexed_ln)
        print(nb_drones_data)
