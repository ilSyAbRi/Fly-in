# from zone import Zone

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
        self.duplicate_list = []

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
        self.duplicate_list = []

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
                # explain chaining
                clean_ln.remove_comments().strip_spaces().remove_empty_lines()
                index_lines = [
                        (i, v)
                        for i, v in enumerate(raw_ln.data, start=1)
                        if v in clean_ln.data
                        ]
                return index_lines

        except OSError as e:
            raise StandardParserError(f"file error -> OSError: {e}")

    def parse_nb_drones(self, clean_indexed_lns: list[tuple]) -> int:
        """
        validate nb drones
        """
        if ':' not in clean_indexed_lns[0][1]:
            raise CustomParserError(f"Line: {clean_indexed_lns[0][0]}"
                                    f"\nError: '{clean_indexed_lns[0][1]}'"
                                    " syntax should have :")
        try:
            name, nb = clean_indexed_lns[0][1].split(':')
            name = name.strip()
            if name != "nb_drones":
                raise CustomParserError(f"Line: {clean_indexed_lns[0][0]}"
                                        f"\nError: '{clean_indexed_lns[0][1]}'"
                                        "nb_drones should be the first one ")
            nb = int(nb)
            if nb < 1:
                raise CustomParserError(f"Line: {clean_indexed_lns[0][0]}"
                                        f"\nError: '{nb}'"
                                        "should be positive")
        except ValueError:
            raise StandardParserError(f"Line: {clean_indexed_lns[0][0]}"
                                      f"\nError : '{clean_indexed_lns[0][1]}'"
                                      " invalid syntax")
        return nb

    def parse_hub(self,nb_line, line: tuple):

        try:
            start_hub, data = line.split(':')
            name, x, y, metadata = data.split()
            x = int(x)
            y = int(y)
            for _n, _x, _y in self.duplicate_list:
                if name == _n or (x == _x and y == _y):
                    raise CustomParserError(f"Line: {nb_line}"
                                            f"\nError: '{line}' "
                                            "duplicate problem"
                                            " check name x y")
            # epxlain deference beteween append and extend
            self.duplicate_list.append((name, x, y))

        except ValueError:
            raise StandardParserError(f"Line: {nb_line}"
                  f"\nError: '{line}'"
                  " Invalid syntax")

    def validate_extract_data(self, clean_indexed_lns: list[tuple]) -> None:

        max_drone = self.parse_nb_drones(clean_indexed_lns)
        
        # explain slicing
        for index, line in clean_indexed_lns[1:]:
            if line.startswith("nb_drones:"):
                raise CustomParserError(f"Line: {index}"
                                        f"\nError: '{line}' duplicate")
            elif line.startswith("start_hub:"):
                self.parse_hub(index, line)
            elif line.startswith("end_hub:"):
                self.parse_hub(index, line)
            elif line.startswith("hub:"):
                self.parse_hub(index, line)
            elif line.startswith("connection:"):
                pass
            else:
                raise CustomParserError(f"line: {index}"
                                        f"\nError: '{line}' unknow line")

    def dispatcher(self) -> None:
        clean_indexed_lns = self.load_raw_input()
        self.validate_extract_data(clean_indexed_lns)
