class Song:
    name = "name"
    tempo: int = 0
    metre = "metre"
    path = "test"

    def __init__(self, path, name="name", tempo=0, metre="metre"):
        self.name = name
        self.tempo = tempo
        self.metre = metre
        self.path = path
