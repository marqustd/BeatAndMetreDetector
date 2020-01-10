class Song:
    name = "name"
    bpm: int = 120
    metre = "4\\4"
    filepath = "test"

    def __init__(self, filepath, name='name', bpm=120, metre='4\\4'):
        self.name = name
        self.bpm = bpm
        self.metre = metre
        self.filepath = filepath
