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


class Note:
    def __init__(self, noteName):
        self.noteName = noteName
        self.noteNumber = Note.toChromaticDegree(noteName)

    def __str__(self):
        return self.noteName

    @classmethod
    def toChromaticDegree(cls, noteName):
        return nameToNum[noteName]

    def sharp(self):
        self.noteNumber = (self.noteNumber + 1) % 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.noteName = notes[self.noteNumber]

    def flat(self):
        self.noteNumber = (self.noteNumber - 1) % 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.noteName = notes[self.noteNumber]


class Chord:
    def __init__(self, notesArray):
        self.notes = notesArray

    def __str__(self):
        chordString = ''
        for note in self.notes:
            chordString = chordString + str(note) + ' '
        return chordString






notesList = [Note('C'), Note('D'), Note('E'), Note('G')]
notesList[1].sharp()
Cadd9 = Chord(notesList)



print Cadd9