from models import Zone, Connection


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
        self.zones: list[Zone] = []
        self.connections: list[Connection] = []

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

    def parse_nb_drones(self, clean_indexed_lns: list[tuple]) -> int:
        """
        validate nb drones
        """
        if ':' not in clean_indexed_lns[0][1]:
            raise CustomParserError(
                f"Line: {clean_indexed_lns[0][0]}"
                f"\nError: '{clean_indexed_lns[0][1]}'"
                " — 'nb_drones:' requires a colon,"
                " use exact syntax: 'nb_drones: <positive_integer>'"
            )
        try:
            name, nb = clean_indexed_lns[0][1].split(':')
            name = name.strip()
            if name != "nb_drones":
                raise CustomParserError(
                    f"Line: {clean_indexed_lns[0][0]}"
                    f"\nError: '{clean_indexed_lns[0][1]}'"
                    " — first line must be 'nb_drones: <positive_integer>',"
                    " no space before ':'"
                )
            nb = int(nb)
            if nb < 1:
                raise CustomParserError(
                    f"Line: {clean_indexed_lns[0][0]}"
                    f"\nError: '{nb}'"
                    " — 'nb_drones' value must be"
                    " a positive integer greater than 0"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {clean_indexed_lns[0][0]}"
                f"\nError: '{clean_indexed_lns[0][1]}'"
                " — 'nb_drones' value must be a valid integer,"
                " e.g: 'nb_drones: 3'"
            )
        return nb

    def parse_hub(self, nb_line: int,
                  line: str, nb_drones: int | None) -> Zone:
        """
        parse each hub
        """
        try:
            _, data = line.split(':')
            parts = data.split(maxsplit=3)
            name, x, y = parts[:3]
            X = int(x)
            Y = int(y)
            if "-" in name:
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    " — zone name cannot contain '-',"
                    " dashes are reserved for connections"
                )
            metadata = parts[3] if len(parts) == 4 else ""
            zone_type, color, max_drones = self.parse_meta_zone(
                        metadata, nb_line, line, nb_drones)
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — invalid zone syntax,"
                " expected: '<type>: <name> <x> <y> [metadata]'"
                " — coordinates x and y must be valid integers"
            )
        for _name, _x, _y in self.duplicate_list:
            if name == _name or (X == _x and Y == _y):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    " — duplicate zone:"
                    " name or coordinates already"
                    " used by another zone"
                )
        self.duplicate_list.append((name, X, Y))
        return Zone(name, X, Y, zone_type, color, max_drones)

    def parse_meta_zone(self, metadata: str, nb_line: int,
                        line: str, nb_drones: int | None) -> tuple:
        """
        parse metadata of each zone
        """
        zone_type = "normal"
        color = "none"
        max_drones = 1
        if metadata == "":
            return zone_type, color, max_drones
        if not metadata.startswith('[') or not metadata.endswith(']'):
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                f" — metadata '{metadata}' must be"
                " wrapped in brackets, use: '[key=value ...]'"
            )
        parts = metadata[1:-1].split()
        if len(parts) > 3 or len(parts) == 0:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — metadata accepts 1 to 3 tags only:"
                " zone=, color=, max_drones="
            )
        try:
            self.dup_meta = []
            for data in parts:
                _, val = data.split("=")
                if data.startswith("zone="):
                    zone_type = self.zone_type_meta(nb_line, line, val)
                elif data.startswith("color="):
                    color = self.color_meta(nb_line, line, val)
                elif data.startswith("max_drones="):
                    max_drones = self.max_drones_meta(nb_line, line,
                                                      val, nb_drones)
                else:
                    raise CustomParserError(
                        f"Line: {nb_line}"
                        f"\nError: '{line}'"
                        " — unknown metadata tag,"
                        " valid tags are:"
                        " 'zone=', 'color=', 'max_drones='"
                    )
            if len(self.dup_meta) != len(set(self.dup_meta)):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    " — duplicate metadata tag found,"
                    " each tag can only appear once per zone"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — invalid metadata syntax,"
                " use: '[key=value key=value]'"
                " with no spaces around '='"
            )
        return zone_type, color, max_drones

    def zone_type_meta(self, nb_line: int, line: str, val: str) -> str:
        """
        validate zone_type metadata
        """
        valid = ["normal", "blocked", "restricted", "priority"]
        if val not in valid:
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: '{line}'"
                " — unknown zone type,"
                " valid types are:"
                " 'normal', 'blocked', 'restricted', 'priority'"
            )
        self.dup_meta.append("zone=")
        return val

    def color_meta(self, nb_line: int, line: str, val: str) -> str:
        """
        validate color metadata
        """
        if val == "":
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: '{line}'"
                " — 'color=' requires a value,"
                " e.g: 'color=red'"
            )
        if not val.isalpha():
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: '{line}'"
                " — color value must contain only letters,"
                " e.g: 'color=red', 'color=blue'"
            )
        self.dup_meta.append("color=")
        return val

    def max_drones_meta(self, nb_line: int, line: str,
                        val: str, nb_drones: int | None) -> int:
        """
        validate max_drones metadata
        """
        value = int(val)
        if value < 1:
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: '{line}'"
                f" — 'max_drones' must be a positive integer"
                f" greater than 0, got '{value}'"
            )
        if nb_drones is not None and value < nb_drones:
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: '{line}'"
                f" — 'max_drones={value}' cannot exceed"
                f" total drone count 'nb_drones={nb_drones}'"
            )
        self.dup_meta.append("max_drones=")
        return value

    def parse_connection(self, nb_line: int, line: str) -> Connection:
        """
        parse connection
        """
        try:
            _, name = line.split(':')
            name1, name2_metadata = name.strip().split('-')
            track_meta_conection = any(c.isspace() for c in name2_metadata)
            if track_meta_conection:
                name2, meta_connection = name2_metadata.split(maxsplit=1)
                max_link_capacity = self.max_link_capacity_meta(
                    meta_connection, nb_line, line)
            else:
                max_link_capacity = 1
                name2 = name2_metadata
            if any(c.isspace() for c in name1):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    f" — zone name '{name1}' cannot contain spaces,"
                    " use exact zone name as defined"
                )
            elif any(c.isspace() for c in name2):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    f" — zone name '{name2}' cannot contain spaces,"
                    " use exact zone name as defined"
                )
            found_name1 = False
            found_name2 = False
            for zone in self.zones:
                if name1 == zone.name:
                    found_name1 = True
                if name2 == zone.name:
                    found_name2 = True
            if found_name1 is not True:
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    f" — zone '{name1}' not found,"
                    " connection must reference"
                    " zones defined above it"
                )
            if found_name2 is not True:
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    f" — zone '{name2}' not found,"
                    " connection must reference"
                    " zones defined above it"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — invalid connection syntax, use:"
                " 'connection: <zone1>-<zone2>"
                " [max_link_capacity=N]'"
            )
        return Connection(name1, name2, max_link_capacity)

    def max_link_capacity_meta(self, meta_connection: str,
                               nb_line: int, line: str) -> int:
        """
        check metadata of connection
        """
        if (not meta_connection.startswith('[')
                or not meta_connection.endswith(']')):
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — connection metadata must be"
                " wrapped in brackets,"
                " use: '[max_link_capacity=N]'"
            )
        meta_connection_part = meta_connection[1:-1].strip().split()
        if len(meta_connection_part) != 1:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — connection metadata accepts"
                " exactly one tag:"
                " 'max_link_capacity=<positive_integer>'"
            )
        meta_connection = meta_connection_part[0]
        if not meta_connection.startswith("max_link_capacity="):
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — unknown connection metadata,"
                " only 'max_link_capacity=<positive_integer>'"
                " is allowed"
            )
        try:
            _, val = meta_connection.split('=')
            value = int(val)
            if value < 1:
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}'"
                    f" — 'max_link_capacity' must be"
                    f" a positive integer greater than 0,"
                    f" got '{val}'"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — 'max_link_capacity' value must be"
                " a valid integer,"
                " e.g: '[max_link_capacity=2]'"
            )
        return value

    def check_count_start_end_hub(self, start_hub_count: int,
                                  end_hub_count: int, nb_line: int,
                                  line: str) -> None:
        """
        check how many start hub i have and how many end hub
        i have and raise error depending on that
        """
        if start_hub_count == 0:
            raise CustomParserError(
                "map must contain exactly one 'start_hub:'"
                " — none found"
            )
        elif end_hub_count == 0:
            raise CustomParserError(
                "map must contain exactly one 'end_hub:'"
                " — none found"
            )
        elif start_hub_count > 1:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — only one 'start_hub:' is allowed"
                " per map, duplicate found here"
            )
        elif end_hub_count > 1:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}'"
                " — only one 'end_hub:' is allowed"
                " per map, duplicate found here"
            )

    def validate_extract_data(self, clean_indexed_lns: list[tuple]) -> None:
        """
        dispatcher of zones only
        """
        nb_drones = self.parse_nb_drones(clean_indexed_lns)
        start_hub_count = 0
        end_hub_count = 0
        for index, line in clean_indexed_lns[1:]:
            if line.startswith("nb_drones:"):
                raise CustomParserError(
                    f"Line: {index}"
                    f"\nError: '{line}'"
                    " — 'nb_drones:' must appear only once"
                    " as the very first line, duplicate found"
                )
            elif line.count(":") != 1:
                raise CustomParserError(
                    f"Line: '{index}'"
                    f"\nError: '{line}'"
                    " — line must contain exactly one ':',"
                    " no space before ':'"
                )
            elif line.startswith("start_hub:"):
                zone = self.parse_hub(index, line, nb_drones)
                self.zones.append(zone)
                start_hub_count += 1
                self.check_count_start_end_hub(start_hub_count, 1, index, line)
            elif line.startswith("end_hub:"):
                zone = self.parse_hub(index, line, nb_drones)
                self.zones.append(zone)
                end_hub_count += 1
                self.check_count_start_end_hub(1, end_hub_count, index, line)
            elif line.startswith("hub:"):
                zone = self.parse_hub(index, line, None)
                self.zones.append(zone)
            elif line.startswith("connection:"):
                connection = self.parse_connection(index, line)
                self.connections.append(connection)
            else:
                raise CustomParserError(
                    f"line: {index}"
                    f"\nError: '{line}'"
                    " — unknown line type, valid types are:"
                    " 'nb_drones:', 'start_hub:',"
                    " 'end_hub:', 'hub:', 'connection:'"
                )
        self.check_count_start_end_hub(start_hub_count,
                                       end_hub_count, index, line)

    def dispatcher(self) -> None:
        """
        the main dispatcher
        """
        clean_indexed_lns = self.load_raw_input()
        self.validate_extract_data(clean_indexed_lns)
