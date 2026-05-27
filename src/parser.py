class CustomParserError(Exception):
    pass


class StandardParserError(Exception):
    pass


class LineCleaner:

    def __init__(self, lines_to_clean: list[str]) -> None:
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
        skip empty lines just to make good structure to work whit
        """
        self.data = [line for line in self.data if line]
        return self


class Parser:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_raw_input(self) -> list[tuple]:
        """
        Load the map file and return cleaned indexed lines.

        Techniques used:
            Methode chaining
            Context manager
            Enumerate
            comprehension

        Returns:
        list[tuple]: List of tuples(index, value).
        """
        try:
            with open(self.file_path, 'r') as file:
                # read file
                content = file.read()

                # check if i have empty file
                if not content.strip():
                    raise CustomParserError(f"Empty File: {self.file_path}")

                # return a list of seperate lines by '\n'
                raw_lines = content.splitlines()

                # instance [clean ln=line]
                clean_ln = LineCleaner(raw_lines)

                # use Method chaining
                # object [comments → spaces → empty]
                clean_ln.remove_comments().strip_spaces().remove_empty_lines()

                # get the right indexing for the clean lines
                # by using raw lines and enumerate
                # and simple condition
                index_lines = [
                        (i, v)
                        for i, v in enumerate(raw_lines, start=1)
                        if v in clean_ln.data
                        ]

                # list of tuple(index,value)
                return index_lines

        except OSError as e:
            raise StandardParserError(f"file error -> OSError: {e}")
