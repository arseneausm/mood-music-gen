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
        notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.noteName = notes[self.noteNumber]

    @classmethod
    def get_interval(cls, note1, note2):
        return (note2.noteNumber - note1.noteNumber) % 12


class Chord:
    def __init__(self, notesArray):
        self.notes = notesArray
        self.root = notesArray[0]

    def __str__(self):
        chordString = ''
        for note in self.notes:
            chordString = chordString + str(note) + ' '
        return chordString

    def get_intervals_in_chord(self):
        intervals = []
        for note in self.notes:
            intervals.append(Note.get_interval(self.root, note))
        return intervals

    def transposeUp(self, steps):
        newChord = []
        for note in self.notes:
            for i in range(steps):
                newChord.append(note.sharp())
        return newChord

    def minor(self):
        noteIntervals = self.get_intervals_in_chord()
        if 4 in noteIntervals:
            i = noteIntervals.index(4)
            self.notes[i].flat()
        # if 11 in noteIntervals:
        #   i = noteIntervals.index(11)
        #  self.notes[i].flat()

    def major(self):
        noteIntervals = self.get_intervals_in_chord()
        if 3 in noteIntervals:
            i = noteIntervals.index(4)
            self.notes[i].sharp()
        # if 10 in noteIntervals:
        #   i = noteIntervals.index(11)
        #   self.notes[i].sharp()


c = Chord([Note('C'), Note('E'), Note('G')]) # C E G
#chordIII = chordI.transposeUp(4).minor() # E G B
#chordIV = chordI.transposeUp(5).major() # F A C
#chordV = chordI.transposeUp(7).major() # G B D
#chordVI = chordI.transposeUp(9).minor() # A C E


# notesList = [Note('C'), Note('Eb'), Note('G')]
# notesList[1].sharp()
# Cmaj7 = Chord(notesList)

# print Cmaj7
# print Cmaj7.get_intervals_in_chord()
# Cmaj7.minor()
# print Cmaj7

# I chord
print c
# ii chord
c.transposeUp(2)
c.minor()
print c
# iii chord
c.transposeUp(2)
print c
# IV chord
c.transposeUp(1)
c.major()
print c
# V chord
c.transposeUp(2)
print c
# vi chord
c.transposeUp(2)
c.minor()
print c
# vii
c.transposeUp(2)