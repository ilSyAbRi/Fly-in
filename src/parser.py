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
                f"\nError: missing ':' in"
                f" '{clean_indexed_lns[0][1]}'"
                "\n — the first line must always be"
                " 'nb_drones: <number>', the colon ':'"
                " is required with no space before it,"
                " example: 'nb_drones: 3'"
            )
        try:
            name, nb = clean_indexed_lns[0][1].split(':')
            name = name.strip()
            if name != "nb_drones":
                raise CustomParserError(
                    f"Line: {clean_indexed_lns[0][0]}"
                    f"\nError: '{clean_indexed_lns[0][1]}'"
                    " is not valid as the first line"
                    "\n — the very first line of the map file"
                    " must always define the number of drones"
                    " using exactly 'nb_drones: <number>',"
                    " no other keyword is allowed here,"
                    " example: 'nb_drones: 5'"
                )
            nb = int(nb)
            if nb < 1:
                raise CustomParserError(
                    f"Line: {clean_indexed_lns[0][0]}"
                    f"\nError: '{nb}' is not a valid drone count"
                    "\n — nb_drones must be a positive integer"
                    " greater than 0, you need at least one"
                    " drone to run the simulation,"
                    " example: 'nb_drones: 3'"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {clean_indexed_lns[0][0]}"
                f"\nError: '{clean_indexed_lns[0][1]}'"
                " has an invalid value for nb_drones"
                "\n — the value after ':' must be a whole number"
                " with no letters or symbols,"
                " example: 'nb_drones: 3'"
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
                    f"\nError: zone name '{name}' in '{line}'"
                    " contains a '-' which is not allowed"
                    "\n — zone names cannot contain dashes"
                    " because dashes are used to separate"
                    " zone names in connections,"
                    " rename this zone without using '-'"
                )
            metadata = parts[3] if len(parts) == 4 else ""
            zone_type, color, max_drones = self.parse_meta_zone(
                        metadata, nb_line, line, nb_drones)
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}' has invalid zone format"
                "\n — a zone must follow this exact format:"
                " '<type>: <name> <x> <y>' where name is a"
                " word without spaces or dashes, x and y are"
                " whole numbers representing coordinates,"
                " example: 'hub: myzone 3 4'"
            )
        for _name, _x, _y in self.duplicate_list:
            if name == _name or (X == _x and Y == _y):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: '{line}' defines a zone"
                    " that already exists"
                    "\n — every zone must have a unique name"
                    " and unique coordinates, check all"
                    " previously defined zones for a conflict"
                    " with this name or these coordinates"
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
                f"\nError: metadata in '{line}'"
                " is not properly wrapped"
                "\n — metadata must start with '[' and end with ']'"
                " with no extra characters outside the brackets,"
                f" got '{metadata}',"
                " example: '[color=red zone=normal max_drones=2]'"
            )
        parts = metadata[1:-1].split()
        if len(parts) > 3 or len(parts) == 0:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: metadata in '{line}'"
                " has an invalid number of tags"
                "\n — metadata must contain between 1 and 3 tags,"
                " no more and no less if brackets are present,"
                " valid tags are 'zone=', 'color=', 'max_drones=',"
                " each appearing at most once,"
                " example: '[color=red zone=normal]'"
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
                        f"\nError: unknown metadata tag '{data}'"
                        f" in '{line}'"
                        "\n — only three tags are allowed inside"
                        " zone metadata: 'zone=<type>',"
                        " 'color=<word>', 'max_drones=<number>',"
                        " any other tag is invalid"
                        " and must be removed"
                    )
            if len(self.dup_meta) != len(set(self.dup_meta)):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: a metadata tag appears"
                    f" more than once in '{line}'"
                    "\n — each tag can only be used once per zone,"
                    " check your metadata for repeated"
                    " 'zone=', 'color=' or 'max_drones=' tags"
                    " and remove the duplicate"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: metadata format is invalid in '{line}'"
                "\n — each tag inside brackets must follow"
                " the format 'key=value' with no spaces around '=',"
                " all tags separated by spaces,"
                " example: '[zone=normal color=red max_drones=2]'"
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
                f"\nError: '{val}' is not a valid zone type"
                f" in '{line}'"
                "\n — the 'zone=' tag only accepts these four values:"
                " 'normal' for standard zones with 1 turn cost,"
                " 'blocked' for zones drones cannot enter,"
                " 'restricted' for zones that cost 2 turns to enter,"
                " 'priority' for zones preferred by the pathfinding"
                " algorithm with 1 turn cost"
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
                f"\nError: 'color=' has no value in '{line}'"
                "\n — the color tag requires a single word value"
                " made of letters only, it is used for visual"
                " display in the terminal or graphical output,"
                " example: 'color=red' or 'color=blue'"
            )
        if not val.isalpha():
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: '{val}' is not a valid color"
                f" value in '{line}'"
                "\n — color must be a single word containing"
                " only letters with no numbers, spaces,"
                " or special characters, it is used purely"
                " for visual display,"
                " example: 'color=green' or 'color=gray'"
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
                f"\nError: 'max_drones={value}'"
                f" is invalid in '{line}'"
                "\n — max_drones defines how many drones"
                " can occupy this zone at the same time"
                " and must be a positive integer greater than 0,"
                " the default value is 1 if this tag"
                " is not specified, example: 'max_drones=2'"
            )
        if nb_drones is not None and value < nb_drones:
            raise CustomParserError(
                f"Line: '{nb_line}'"
                f"\nError: 'max_drones={value}' in '{line}'"
                f" cannot be greater than the total number"
                f" of drones which is 'nb_drones={nb_drones}'"
                "\n — it makes no sense to allow more drones"
                " in a zone than the total number of drones"
                " in the simulation, reduce max_drones"
                f" to a value between 1 and {nb_drones}"
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
                    f"\nError: zone name '{name1}' in '{line}'"
                    " contains spaces which are not allowed"
                    "\n — zone names must be a single word"
                    " with no spaces, check the zone definitions"
                    " above and use the exact name as it was defined"
                )
            elif any(c.isspace() for c in name2):
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: zone name '{name2}' in '{line}'"
                    " contains spaces which are not allowed"
                    "\n — zone names must be a single word"
                    " with no spaces, check the zone definitions"
                    " above and use the exact name as it was defined"
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
                    f"\nError: zone '{name1}' used in '{line}'"
                    " was never defined"
                    "\n — connections can only link zones that"
                    " have been defined above using 'hub:',"
                    " 'start_hub:', or 'end_hub:',"
                    " check your spelling or add the missing"
                    " zone definition before this line"
                )
            if found_name2 is not True:
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: zone '{name2}' used in '{line}'"
                    " was never defined"
                    "\n — connections can only link zones that"
                    " have been defined above using 'hub:',"
                    " 'start_hub:', or 'end_hub:',"
                    " check your spelling or add the missing"
                    " zone definition before this line"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: '{line}' has invalid connection format"
                "\n — a connection must follow this exact format:"
                " 'connection: <zone1>-<zone2>' where zone1 and"
                " zone2 are names of previously defined zones"
                " separated by a single '-', optionally followed"
                " by '[max_link_capacity=<number>]',"
                " example: 'connection: start-goal' or"
                " 'connection: zoneA-zoneB [max_link_capacity=2]'"
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
                f"\nError: connection metadata in '{line}'"
                " is not properly wrapped"
                "\n — connection metadata must start with '['"
                " and end with ']' with no extra characters"
                f" outside, got '{meta_connection}',"
                " example: '[max_link_capacity=2]'"
            )
        meta_connection_part = meta_connection[1:-1].strip().split()
        if len(meta_connection_part) != 1:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: connection metadata in '{line}'"
                " has too many or too few tags"
                "\n — connection metadata accepts exactly one tag"
                " which is 'max_link_capacity=<number>',"
                " remove any extra content from the brackets,"
                " example: '[max_link_capacity=2]'"
            )
        meta_connection = meta_connection_part[0]
        if not meta_connection.startswith("max_link_capacity="):
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: unknown connection metadata tag"
                f" in '{line}'"
                "\n — the only allowed tag in connection metadata"
                " is 'max_link_capacity=<number>' which defines"
                " how many drones can use this connection"
                " at the same time, the default is 1"
                " if no metadata is provided,"
                " example: '[max_link_capacity=3]'"
            )
        try:
            _, val = meta_connection.split('=')
            value = int(val)
            if value < 1:
                raise CustomParserError(
                    f"Line: {nb_line}"
                    f"\nError: 'max_link_capacity={val}'"
                    f" in '{line}' is not valid"
                    "\n — max_link_capacity defines how many drones"
                    " can travel through this connection"
                    " at the same time and must be a positive"
                    " integer greater than 0, the default is 1,"
                    " example: '[max_link_capacity=2]'"
                )
        except ValueError:
            raise StandardParserError(
                f"Line: {nb_line}"
                f"\nError: 'max_link_capacity' value in '{line}'"
                " is not a valid number"
                "\n — the value after '=' must be a whole positive"
                " integer with no letters or symbols,"
                " example: '[max_link_capacity=2]'"
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
                "Error: no 'start_hub:' found in this map"
                "\n — every map must have exactly one starting zone"
                " defined using 'start_hub: <name> <x> <y>',"
                " this is where all drones begin the simulation,"
                " add a start zone to your map file"
            )
        elif end_hub_count == 0:
            raise CustomParserError(
                "Error: no 'end_hub:' found in this map"
                " — every map must have exactly one ending zone"
                " defined using 'end_hub: <name> <x> <y>',"
                " this is the destination all drones must reach"
                " to complete the simulation,"
                " add an end zone to your map file"
            )
        elif start_hub_count > 1:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: second 'start_hub:' found in '{line}'"
                "\n — a map can only have one starting zone,"
                " the first 'start_hub:' was already defined"
                " earlier in the file, remove this duplicate"
                " or convert it to a regular 'hub:' zone"
            )
        elif end_hub_count > 1:
            raise CustomParserError(
                f"Line: {nb_line}"
                f"\nError: second 'end_hub:' found in '{line}'"
                "\n — a map can only have one ending zone,"
                " the first 'end_hub:' was already defined"
                " earlier in the file, remove this duplicate"
                " or convert it to a regular 'hub:' zone"
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
                    f"\nError: 'nb_drones:' found again in '{line}'"
                    "\n — 'nb_drones:' must appear only once"
                    " and must be the very first line"
                    " of the map file, remove this duplicate line"
                )
            elif line.count(":") != 1:
                raise CustomParserError(
                    f"Line: '{index}'"
                    f"\nError: '{line}' contains"
                    " more than one ':'"
                    "\n — every line in the map file must have"
                    " exactly one ':' separating the keyword"
                    " from its value with no space before ':',"
                    " check for extra colons in this line"
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
                    f"line: {index}"
                    f"\nError: '{line}' starts with"
                    " an unknown keyword"
                    "\n — the map file only accepts these"
                    " line types: 'nb_drones:' for drone count"
                    " on line 1, 'start_hub:' for the start zone,"
                    " 'end_hub:' for the end zone,"
                    " 'hub:' for regular zones,"
                    " 'connection:' for links between zones"
                    "\n — check your spelling and make sure"
                    " there is no space before ':'"
                )
        self.check_count_start_end_hub(start_hub_count,
                                       end_hub_count, index, line)

    def dispatcher(self) -> None:
        """
        the main dispatcher
        """
        clean_indexed_lns = self.load_raw_input()
        self.validate_extract_data(clean_indexed_lns)
