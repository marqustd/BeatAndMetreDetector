class Song:
    name = "name"
    bpm: int = 0
    metre = "metre"
    filepath = "test"

    def __init__(self, filepath, name='name', bpm=0, metre='metre'):
        self.name = name
        self.bpm = bpm
        self.metre = metre
        self.filepath = filepath
