class Song:
    name = "name"
    bpm: int = 120
    metre = "4/4"
    filepath = "test"

    def __init__(self, name, bpm, metre, filepath):
        self.name = name
        self.bpm = bpm
        self.metre = metre
        self.filepath = filepath

    def __init__(self, filepath):
        self.filepath = filepath
        self.name = filepath
