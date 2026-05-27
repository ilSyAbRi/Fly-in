class CustomParserError(Exception):
    """
    class just for custom error
    """
    pass


class StandardParserError(Exception):
    """
    class just for standar error
    """
    pass


class LineCleaner:
    """
    help class
    help me clean lines by methodes and give me permession
    for using chaining
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

    def load_raw_input(self) -> list[tuple]:
        """
        Load the map file and return cleaned indexed lines.

        Techniques used:
            Methode chaining
            Context manager
            Enumerate
            comprehension

        What is the clean lines ?
        
        that line pass of this 3 process
        
            remove comments
            strip spaces
            remove empty lines

        What is raw lines ?

        that need at least one of this process
            
            remove comments
            strip spaces
            remove empty lines

        Returns:
        list[tuple]: List of tuples(index, value) List=clean lines.
        """
        try:
            with open(self.file_path, 'r') as file:
                # read file and store the content
                content = file.read()

                # check if i have empty file
                if not content.strip():
                    raise CustomParserError(f"Empty File: {self.file_path}")

                # return a list of seperate lines by '\n'
                lines = content.splitlines()

                # instance [raw ln=line]
                raw_ln = LineCleaner(lines)

                # use Method chaining
                # object [comments → spaces] = raw line
                # still need remove empty lines to be clean lines
                # we do remove comments and strip spaces
                # to get the right value in raw lines
                # that are exactly like clean lines
                # no additional space there no comment
                # we keep empty lines to keep the order
                raw_ln.remove_comments().strip_spaces()
                
                # instance [clean ln=line]
                clean_ln = LineCleaner(lines)

                # use Method chaining
                # object [comments → spaces -> empty lines] = clean lines
                clean_ln.remove_comments().strip_spaces().remove_empty_lines()

                # get the right indexing for the clean lines
                # by using raw lines and enumerate
                # and simple condition
                index_lines = [
                        (i, v)
                        for i, v in enumerate(raw_ln.data, start=1)
                        if v in clean_ln.data
                        ]

                # list of tuple(index,value)
                return index_lines

        # OSError contain all error that my open can come with
        except OSError as e:
            raise StandardParserError(f"file error -> OSError: {e}")
