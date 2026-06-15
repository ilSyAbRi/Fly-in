from models import Zone

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
        self.duplicate_list: list[tuple] = []
        self.dup_meta: list = []
        self.zones: list[tuple] = []

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

    def parse_hub(self, nb_line: int, line: str, nb_drones: int) -> None:
        """
        parse each hub
        """
        try:
            _, data = line.split(':')
            parts = data.split(maxsplit=3)
            name, x, y = parts[:3]
            metadata = parts[3] if len(parts) == 4 else ""
            zone_type, color, max_drones = self.parse_metadata(
                        metadata, nb_line, line, nb_drones)

            X = int(x)
            Y = int(y)
        except ValueError:
            raise StandardParserError(f"Line: {nb_line}"
                                      f"\nError: '{line}'"
                                      " cordinates should"
                                      " be number")
        for _name, _x, _y in self.duplicate_list:
            if name == _name or (X == _x and Y == _y):
                raise CustomParserError(f"Line: {nb_line}"
                                        f"\nError: '{line}' "
                                        "duplicate problem"
                                        " check name x y")
        self.duplicate_list.append((name, X, Y))
        return Zone(name, X, Y, zone_type, color, max_drones)

    def zone_type_meta(self, nb_line, line ,val: str):
        """
        validate zone_type metadata
        """
        valid = ["normal", "blocked", "restricted"]
        if val not in valid:
            raise CustomParserError(f"Line: '{nb_line}'"
                                    f"\nError: '{line}'"
                                    f" unknown zone")
        self.dup_meta.append("zone=")
        return val

    def color_meta(self, nb_line, line, val: str):
        """
        validate color metadata
        """
        if val == "":
            raise CustomParserError(f"Line: '{nb_line}'"
                                    f"\nError: '{line}'"
                                    " empty metadata")
        if not val.isalpha():
            raise CustomParserError(f"Line: '{nb_line}'"
                                    f"\nError: '{line}'"
                                    " color should be "
                                    "only alphabitic")
        self.dup_meta.append("color=")
        return val

    def max_drones_meta(self, nb_line, line, val: str, nb_drones: int):
        """
        validate max_drones metadata
        """
        value = int(val)
        if value < 1:
            raise CustomParserError(f"Line: '{nb_line}'"
                                    f"\nError: '{line}'"
                                    f" '{value}' should"
                                    " be positive")
        if nb_drones is not None and value > nb_drones:
            raise CustomParserError(f"Line: '{nb_line}'"
                                    f"\nError: '{line}'"
                                    f" '{value}' should be'"
                                    "more or equal nb_drones:")
        self.dup_meta.append("max_drones=")
        return value

    def parse_metadata(self, metadata: str, nb_line: int,
                       line: str, nb_drones: int) -> tuple:
        """
        parse metadata of each zone
        """
        zone_type = "normal"
        color = "none"
        max_drones = 1
        if metadata == "":
            return zone_type, color, max_drones
        if not metadata.startswith('[') or not metadata.endswith(']'):
            raise CustomParserError(f"Line: {nb_line}"
                                    f"\nError: '{line}'"
                                    " metadata should start"
                                    " and end with '[]'")
        metadata = metadata[1:-1]
        parts = metadata.split()
        if len(parts) > 3 or metadata == "":
            raise CustomParserError(f"Line: {nb_line}"
                                    f"\nError: '{line}'"
                                    " not valid number"
                                    " of element in metadata")
        try:
            dup_meta = []
            for data in parts:
                _, val = data.split("=")
                if data.startswith("zone="):
                    zone_type = self.zone_type_meta(nb_line, line, val)
                elif data.startswith("color="):
                    color = self.color_meta(nb_line, line, val)
                elif data.startswith("max_drones="):
                    max_drones = self.max_drones_meta(nb_line, line, val, nb_drones)
                else:
                    raise CustomParserError(f"Line: {nb_line}"
                                            f"\nError: '{line}'"
                                            " unknown line")
                if len(dup_meta) != len(set(dup_meta)):
                    raise CustomParserError(f"Line: {nb_line}"
                                            f"\nError: '{line}'"
                                            " duplicate problem"
                                            " in metadata")
        except ValueError:
            raise StandardParserError(f"Line: {nb_line}"
                                      f"\nError: '{line}'"
                                      " invalid syntax")
        return zone_type, color, max_drones

    def validate_extract_data(self, clean_indexed_lns: list[tuple]) -> None:
        """
        dispatcher of zones only
        """
        nb_drones = self.parse_nb_drones(clean_indexed_lns)
        count = 0
        for index, line in clean_indexed_lns[1:]:
            if line.startswith("nb_drones:"):
                raise CustomParserError(f"Line: {index}"
                                        f"\nError: '{line}' duplicate")
            elif line.startswith("start_hub:"):
                zone = self.parse_hub(index, line, nb_drones)
                self.zones.append(zone)
                count += 1
            elif line.startswith("end_hub:"):
                zone = self.parse_hub(index, line, nb_drones)
                self.zones.append(zone)
                count += 1
            elif line.startswith("hub:"):
                zone = self.parse_hub(index, line, None)
                self.zones.append(zone)
            elif line.startswith("connection:"):
                pass
            else:
                raise CustomParserError(f"line: {index}"
                                        f"\nError: '{line}' unknow line")
        if count != 2:
            raise CustomParserError("it should be one"
                                    " start hub and one end hub")

    def dispatcher(self) -> None:
        """
        the main dispatcher
        """
        clean_indexed_lns = self.load_raw_input()
        self.validate_extract_data(clean_indexed_lns)
