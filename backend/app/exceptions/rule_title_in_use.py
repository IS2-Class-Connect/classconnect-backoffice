class TitleAlreadyInUse(Exception):
    def __init__(self):
        super().__init__("Rule title already in use")
