class PersonalError(Exception):
    pass


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_raw_input(self):
        try:
            with open(self.file_path, 'r') as file:
                # read file object as file and return it as a list of newline
                return file.read().splitlines()
        except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
            raise PersonalError(f"file error: {e}")
