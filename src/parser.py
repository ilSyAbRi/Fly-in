class PersonalError(Exception):
    pass

class parser:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_raw_input(self):
        try:
            with open(self.file_path, 'r') as file:
                content = file.readlines()
                return content
        except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
            raise PersonalError(f"file error: {e}")
