class PersonalError(Exception):
    pass


class clean_lines_helper:

    def __init__(self, lines_to_clean: list[str]) -> None:
        self.lines = lines_to_clean


    def remove_comment(self) -> list[str]:
        """
        clean lines form comment any comment
        """
        self.lines = [line.split("#")[0] for line in self.lines]
        return self


    def clean_lines_spaces(self) -> list[str]:
        """
        clean lines from front and up spaces:
        """
        self.lines: list[str] = [line.strip() for line in self.lines]
        return self


    def empty_lines (self):
        """
        skip empty lines just to make good structure to work whit
        """
        self.lines: list[str] = [line for line in self.lines if line]
        return self


class Parser:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_raw_input(self) -> list[str]:
        """
        Load the map file and return cleaned lines.

        Returns:
        list[str]: List of non-empty stripped lines from the file.
        """
        try:
            with open(self.file_path, 'r') as file:

                lines = file.read().splitlines()

                helper = clean_lines_helper(lines)

                return helper.remove_comment().clean_lines_spaces().empty_lines().lines


        except OSError as e:
            raise PersonalError(f"file error -> OSError: {e}")
        except Exception as e:
            raise PersonalError(f"file error -> ExceptionError: {e}")
