class PersonalError(Exception):
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

    def load_raw_input(self) -> list[str]:
        """
        Load the map file and return cleaned lines.

        Techniques used:
            Methode chaining
            Context manager

        Returns:
        list[str]: List of non-empty stripped lines from the file.
        """
        try:
            with open(self.file_path, 'r') as file:
                # use Method chaining
                lines = file.read().splitlines()

                helper = LineCleaner(lines)

                # object [comments → spaces → empty]
                helper.remove_comments().strip_spaces().remove_empty_lines()

                # .data to access to the object helper
                return helper.data

        except OSError as e:
            raise PersonalError(f"file error -> OSError: {e}")
