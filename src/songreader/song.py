class Song:
    name = "name"
    tempo: int = 0
    metre: int = 0
    path = "test"

    def __init__(self, path, name="name", tempo=0, metre=0):
        self.name = name
        self.tempo = tempo
        self.metre = metre
        self.path = path
