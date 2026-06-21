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
        self.nb_drones: int = 0

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
                f"Line: {clean_indexed_lns[0][0]}\n"
                f"Error: missing ':' in nb_drones definition\n"
                f"Got:   '{clean_indexed_lns[0][1]}'\n"
                f"Why:   the colon ':' is required to separate\n"
                f"       the keyword from its value,\n"
                f"       no space is allowed before ':'\n"
                f"Fix:   'nb_drones: 3'"
            )
        try:
            name, nb = clean_indexed_lns[0][1].split(':')
            name = name.strip()
            if name != "nb_drones":
                raise CustomParserError(
                    f"Line: {clean_indexed_lns[0][0]}\n"
                    f"Error: first line must be 'nb_drones:'\n"
                    f"Got:   '{clean_indexed_lns[0][1]}'\n"
                    f"Why:   the very first line of every map file\n"
                    f"       must define the total number of drones\n"
                    f"       no other keyword is allowed on line 1\n"
                    f"Fix:   'nb_drones: 5'"
                )
            nb = int(nb)
            if nb < 1:
                raise CustomParserError(
                    f"Line: {clean_indexed_lns[0][0]}\n"
                    f"Error: nb_drones must be greater than 0\n"
                    f"Got:   '{nb}'\n"
                    f"Why:   the simulation requires at least one drone\n"
                    f"       to run, a value of 0 or less makes no sense\n"
                    f"Fix:   'nb_drones: 3'"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {clean_indexed_lns[0][0]}\n"
                f"Error: nb_drones value must be a whole number\n"
                f"Got:   '{clean_indexed_lns[0][1]}'\n"
                f"Why:   the value after ':' must be a positive integer\n"
                f"       with no letters, spaces, or special characters\n"
                f"Fix:   'nb_drones: 3'"
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
                    f"Line: {nb_line}\n"
                    f"Error: zone name cannot contain '-'\n"
                    f"Got:   '{name}'\n"
                    f"Why:   dashes are used to separate zone names\n"
                    f"       in connection definitions like 'zone1-zone2'\n"
                    f"       using '-' in a name would break connection parsing\n"
                    f"Fix:   rename the zone without using '-'"
                )
            metadata = parts[3] if len(parts) == 4 else ""
            zone_type, color, max_drones = self.parse_meta_zone(
                        metadata, nb_line, line, nb_drones)
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}\n"
                f"Error: invalid zone format\n"
                f"Got:   '{line}'\n"
                f"Why:   a zone must have a name and two integer\n"
                f"       coordinates x and y after the keyword,\n"
                f"       any non-integer value for x or y is invalid\n"
                f"Fix:   'hub: myzone 3 4' or\n"
                f"       'hub: myzone 3 4 [color=red zone=normal]'"
            )
        for _name, _x, _y in self.duplicate_list:
            if name == _name or (X == _x and Y == _y):
                raise CustomParserError(
                    f"Line: {nb_line}\n"
                    f"Error: zone name or coordinates already used\n"
                    f"Got:   '{line}'\n"
                    f"Why:   every zone must have a unique name\n"
                    f"       and unique coordinates, two zones cannot\n"
                    f"       share the same name or the same x and y\n"
                    f"Fix:   use a different name or different coordinates"
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
                f"Line: {nb_line}\n"
                f"Error: metadata must be wrapped in '[' and ']'\n"
                f"Got:   '{metadata}'\n"
                f"Why:   metadata is optional but if present it must\n"
                f"       start with '[' and end with ']' with no extra\n"
                f"       characters outside the brackets\n"
                f"Fix:   '[color=red zone=normal max_drones=2]'"
            )
        parts = metadata[1:-1].split()
        if len(parts) > 3 or len(parts) == 0:
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: metadata must have between 1 and 3 tags\n"
                f"Got:   '{metadata}'\n"
                f"Why:   empty brackets '[]' are not allowed,\n"
                f"       and only three tags exist: zone=, color=,\n"
                f"       max_drones= so more than 3 is always invalid\n"
                f"Fix:   '[zone=normal color=red]'"
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
                        f"Line: {nb_line}\n"
                        f"Error: unknown metadata tag '{data}'\n"
                        f"Got:   '{metadata}'\n"
                        f"Why:   only three tags are allowed inside\n"
                        f"       zone metadata brackets\n"
                        f"       any other tag name is invalid\n"
                        f"Fix:   use only 'zone=', 'color=', 'max_drones='"
                    )
            if len(self.dup_meta) != len(set(self.dup_meta)):
                raise CustomParserError(
                    f"Line: {nb_line}\n"
                    f"Error: duplicate tag found in metadata\n"
                    f"Got:   '{metadata}'\n"
                    f"Why:   each tag can only appear once per zone,\n"
                    f"       having 'color=red color=blue' for example\n"
                    f"       is ambiguous and not allowed\n"
                    f"Fix:   remove the duplicate tag"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}\n"
                f"Error: invalid metadata format\n"
                f"Got:   '{metadata}'\n"
                f"Why:   each tag must follow the format 'key=value'\n"
                f"       with no spaces around '=' and no missing value,\n"
                f"       tags must be separated by spaces\n"
                f"Fix:   '[zone=normal color=red max_drones=2]'"
            )
        return zone_type, color, max_drones

    def zone_type_meta(self, nb_line: int, line: str, val: str) -> str:
        """
        validate zone_type metadata
        """
        valid = ["normal", "blocked", "restricted", "priority"]
        if val not in valid:
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: unknown zone type '{val}'\n"
                f"Got:   '{val}'\n"
                f"Why:   the 'zone=' tag only accepts four specific\n"
                f"       values that define the zone behavior:\n"
                f"       'normal'     costs 1 turn to enter (default)\n"
                f"       'blocked'    drones cannot enter this zone\n"
                f"       'restricted' costs 2 turns to enter\n"
                f"       'priority'   costs 1 turn, preferred by pathfinding\n"
                f"Fix:   'zone=normal' or 'zone=blocked' or\n"
                f"       'zone=restricted' or 'zone=priority'"
            )
        self.dup_meta.append("zone=")
        return val

    def color_meta(self, nb_line: int, line: str, val: str) -> str:
        """
        validate color metadata
        """
        if val == "":
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: 'color=' has no value\n"
                f"Got:   'color='\n"
                f"Why:   the color tag is used for visual display\n"
                f"       in the terminal or graphical output,\n"
                f"       it requires a single word made of letters only\n"
                f"Fix:   'color=red' or 'color=blue' or 'color=green'"
            )
        if not val.isalpha():
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: color value must contain letters only\n"
                f"Got:   '{val}'\n"
                f"Why:   color is used purely for visual display\n"
                f"       and must be a single word with no numbers,\n"
                f"       spaces, dashes, or any special characters\n"
                f"Fix:   'color=green' or 'color=gray' or 'color=red'"
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
                f"Line: {nb_line}\n"
                f"Error: max_drones must be greater than 0\n"
                f"Got:   'max_drones={value}'\n"
                f"Why:   max_drones defines how many drones can\n"
                f"       occupy this zone at the same time,\n"
                f"       a value of 0 or less makes no sense,\n"
                f"       the default is 1 if this tag is not specified\n"
                f"Fix:   'max_drones=2'"
            )
        if nb_drones is not None and value < nb_drones:
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: max_drones cannot exceed total nb_drones\n"
                f"Got:   max_drones={value}, nb_drones={nb_drones}\n"
                f"Why:   allowing more drones in a zone than the total\n"
                f"       number of drones in the simulation makes no sense\n"
                f"Fix:   use a value between 1 and {nb_drones}"
            )
        self.dup_meta.append("max_drones=")
        return value

    def parse_connection(self, nb_line: int, line: str) -> Connection:
        """
        parse connection
        """
        try:
            _, name = line.split(':')
            name = name.strip()
            name1, name2_metadata = name.split('-')
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
                    f"Line: {nb_line}\n"
                    f"Error: zone name '{name1}' contains spaces\n"
                    f"Got:   '{name1}'\n"
                    f"Why:   zone names must be a single word with\n"
                    f"       no spaces, the '-' separates the two zone\n"
                    f"       names so any space breaks the parsing\n"
                    f"Fix:   use the exact zone name as it was defined"
                )
            elif any(c.isspace() for c in name2):
                raise CustomParserError(
                    f"Line: {nb_line}\n"
                    f"Error: zone name '{name2}' contains spaces\n"
                    f"Got:   '{name2}'\n"
                    f"Why:   zone names must be a single word with\n"
                    f"       no spaces, the '-' separates the two zone\n"
                    f"       names so any space breaks the parsing\n"
                    f"Fix:   use the exact zone name as it was defined"
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
                    f"Line: {nb_line}\n"
                    f"Error: zone '{name1}' was never defined\n"
                    f"Got:   '{line}'\n"
                    f"Why:   connections can only link zones that exist,\n"
                    f"       '{name1}' was not found in any hub definition\n"
                    f"       above this line in the file\n"
                    f"Fix:   define '{name1}' using 'hub:', 'start_hub:',\n"
                    f"       or 'end_hub:' before this connection line"
                )
            if found_name2 is not True:
                raise CustomParserError(
                    f"Line: {nb_line}\n"
                    f"Error: zone '{name2}' was never defined\n"
                    f"Got:   '{line}'\n"
                    f"Why:   connections can only link zones that exist,\n"
                    f"       '{name2}' was not found in any hub definition\n"
                    f"       above this line in the file\n"
                    f"Fix:   define '{name2}' using 'hub:', 'start_hub:',\n"
                    f"       or 'end_hub:' before this connection line"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}\n"
                f"Error: invalid connection format\n"
                f"Got:   '{line}'\n"
                f"Why:   a connection must have exactly two zone names\n"
                f"       separated by a single '-' after 'connection:',\n"
                f"       both names must be defined zones\n"
                f"Fix:   'connection: zone1-zone2' or\n"
                f"       'connection: zone1-zone2 [max_link_capacity=2]'"
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
                f"Line: {nb_line}\n"
                f"Error: connection metadata must be wrapped in '[' and ']'\n"
                f"Got:   '{meta_connection}'\n"
                f"Why:   metadata is optional but if present it must\n"
                f"       start with '[' and end with ']' with no extra\n"
                f"       characters or spaces outside the brackets\n"
                f"Fix:   '[max_link_capacity=2]'"
            )
        meta_connection_part = meta_connection[1:-1].strip().split()
        if len(meta_connection_part) != 1:
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: connection metadata must have exactly one tag\n"
                f"Got:   '{meta_connection}'\n"
                f"Why:   connection metadata only supports one tag\n"
                f"       which is 'max_link_capacity=<number>',\n"
                f"       empty brackets or multiple tags are not allowed\n"
                f"Fix:   '[max_link_capacity=2]'"
            )
        meta_connection = meta_connection_part[0]
        if not meta_connection.startswith("max_link_capacity="):
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: unknown connection metadata tag\n"
                f"Got:   '{meta_connection}'\n"
                f"Why:   the only allowed tag in connection metadata\n"
                f"       is 'max_link_capacity=<number>' which defines\n"
                f"       how many drones can use this connection at once,\n"
                f"       the default value is 1 if no metadata is provided\n"
                f"Fix:   '[max_link_capacity=2]'"
            )
        try:
            _, val = meta_connection.split('=')
            value = int(val)
            if value < 1:
                raise CustomParserError(
                    f"Line: {nb_line}\n"
                    f"Error: max_link_capacity must be greater than 0\n"
                    f"Got:   '{val}'\n"
                    f"Why:   max_link_capacity defines how many drones\n"
                    f"       can travel through this connection at once,\n"
                    f"       a value of 0 or less makes no sense,\n"
                    f"       the default is 1 if no metadata is provided\n"
                    f"Fix:   '[max_link_capacity=2]'"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}\n"
                f"Error: max_link_capacity value must be a whole number\n"
                f"Got:   '{meta_connection}'\n"
                f"Why:   the value after '=' must be a positive integer\n"
                f"       with no letters, spaces, or special characters\n"
                f"Fix:   '[max_link_capacity=2]'"
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
                "Error: no 'start_hub:' found in this map\n"
                "Why:   every map must have exactly one starting zone\n"
                "       this is where all drones begin the simulation,\n"
                "       without it the simulation cannot start\n"
                "Fix:   add 'start_hub: <name> <x> <y>' to your map"
            )
        elif end_hub_count == 0:
            raise CustomParserError(
                "Error: no 'end_hub:' found in this map\n"
                "Why:   every map must have exactly one ending zone,\n"
                "       this is the destination all drones must reach,\n"
                "       without it the simulation has no goal\n"
                "Fix:   add 'end_hub: <name> <x> <y>' to your map"
            )
        elif start_hub_count > 1:
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: only one 'start_hub:' is allowed\n"
                f"Got:   '{line}'\n"
                f"Why:   a map can only have one starting zone,\n"
                f"       the first 'start_hub:' was already defined\n"
                f"       earlier in the file, having two start zones\n"
                f"       makes the simulation ambiguous\n"
                f"Fix:   remove this duplicate or convert it to 'hub:'"
            )
        elif end_hub_count > 1:
            raise CustomParserError(
                f"Line: {nb_line}\n"
                f"Error: only one 'end_hub:' is allowed\n"
                f"Got:   '{line}'\n"
                f"Why:   a map can only have one ending zone,\n"
                f"       the first 'end_hub:' was already defined\n"
                f"       earlier in the file, having two end zones\n"
                f"       makes the simulation ambiguous\n"
                f"Fix:   remove this duplicate or convert it to 'hub:'"
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
                    f"Line: {index}\n"
                    f"Error: 'nb_drones:' appears more than once\n"
                    f"Got:   '{line}'\n"
                    f"Why:   'nb_drones:' must appear only once\n"
                    f"       and must be the very first line of the file,\n"
                    f"       having it twice creates a conflict\n"
                    f"Fix:   remove this duplicate 'nb_drones:' line"
                )
            elif line.count(":") != 1:
                raise CustomParserError(
                    f"Line: {index}\n"
                    f"Error: line must have exactly one ':'\n"
                    f"Got:   '{line}'\n"
                    f"Why:   every line uses ':' to separate the keyword\n"
                    f"       from its value, having more than one ':'\n"
                    f"       or none at all breaks the line parsing\n"
                    f"Fix:   check for extra or missing ':' in this line"
                )
            elif line.startswith("start_hub:"):
                zone = self.parse_hub(index, line, nb_drones)
                self.zones.append(zone)
                start_hub_count += 1
                self.check_count_start_end_hub(
                    start_hub_count, 1, index, line)
            elif line.startswith("end_hub:"):
                zone = self.parse_hub(index, line, nb_drones)
                self.zones.append(zone)
                end_hub_count += 1
                self.check_count_start_end_hub(
                    1, end_hub_count, index, line)
            elif line.startswith("hub:"):
                zone = self.parse_hub(index, line, None)
                self.zones.append(zone)
            elif line.startswith("connection:"):
                connection = self.parse_connection(index, line)
                self.connections.append(connection)
            else:
                raise CustomParserError(
                    f"Line: {index}\n"
                    f"Error: unknown keyword in this line\n"
                    f"Got:   '{line}'\n"
                    f"Why:   the map file only accepts five specific\n"
                    f"       line types, anything else is invalid\n"
                    f"Fix:   use one of these:\n"
                    f"       'nb_drones:'  — drone count, the first one\n"
                    f"       'start_hub:'  — the starting zone\n"
                    f"       'end_hub:'    — the ending zone\n"
                    f"       'hub:'        — a regular zone\n"
                    f"       'connection:' — a link between two zones"
                )
        self.check_count_start_end_hub(start_hub_count,
                                       end_hub_count, index, line)

    def dispatcher(self) -> None:
        """
        the main dispatcher
        """
        clean_indexed_lns = self.load_raw_input()
        self.validate_extract_data(clean_indexed_lns)

