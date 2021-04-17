class Note:
    def __init__(self, noteName):
        self.noteName = noteName
        self.noteNumber = Note.toChromaticDegree(noteName)

    @classmethod
    def toChromaticDegree(cls, noteName):
        nameToNum = {'C': 0,
                     'C#': 1,
                     'Db': 1,
                     'D': 2,
                     'D#': 3,
                     'Eb': 3,
                     'E': 4,
                     'E#': 5,
                     'F': 5,
                     'F#': 6,
                     'Gb': 6,
                     'G': 7,
                     'G#': 8,
                     'Ab': 8,
                     'A': 9,
                     'A#': 10,
                     'Bb': 10,
                     'B': 11,
                     'Cb': 11,
                     'C2': 12
                     }
        return nameToNum[noteName]

