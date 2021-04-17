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
numToName = {0: 'C',

             1: 'Db',
             2: 'D',

             3: 'Eb',
             4: 'E',

             5: 'F',
             6: 'F#',

             7: 'G',
             8: 'G#',

             9: 'A',

             10: 'Bb',
             11: 'B',

             12: 'C2'
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


modes = {1: [Note('C'), Note('D'), Note('E'), Note('F'), Note('G'), Note('A'), Note('B')],  # ionian/major
         2: [Note('D'), Note('E'), Note('F'), Note('G'), Note('A'), Note('B'), Note('C')],  # dorian / minor-ish
         3: [Note('E'), Note('F'), Note('G'), Note('A'), Note('B'), Note('C'), Note('D')],  # phrygian / minor-creepy
         4: [Note('F'), Note('G'), Note('A'), Note('B'), Note('C'), Note('D'), Note('E')],  # lydian / major!
         5: [Note('G'), Note('A'), Note('B'), Note('C'), Note('D'), Note('E'), Note('F')],  # mixolydian / major-minor
         6: [Note('A'), Note('B'), Note('C'), Note('D'), Note('E'), Note('F'), Note('G')],  # aoelian / minor
         7: [Note('B'), Note('C'), Note('D'), Note('E'), Note('F'), Note('G'), Note('A')],  # locrian / minor-creepy
         }
# modes go bright to dark (lower index : more "major")
majorModes = [modes[4],  # lydian
              modes[1],  # ionian
              modes[5]  # mixolydian
              ]

# modes go bright to dark (higher index : much darker)
minorModes = [modes[5],  # mixolydian
              modes[2],  # dorian
              modes[6],  # aoelian
              modes[3],  # phrygian
              modes[7]  # locrian
              ]


class Chord:

    def changeDegree(self, degree, sharp):
        noteIntervals = self.get_intervals_in_chord()
        if degree in noteIntervals:
            i = noteIntervals.index(degree)
            if sharp:
                self.notes[i].sharp()
                return True
            else:
                self.notes[i].flat()
                return True

    # ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    def __init__(self, modeNum, rootDegree, numNotes):
        # rootDegree indexed at 1 (for the sake of ii VI I etc)
        self.mode = modes[modeNum]
        noteDegree = rootDegree - 1
        self.root = self.mode[noteDegree]
        self.notes = []
        nextNote = self.mode[noteDegree]
        for i in range(numNotes):
            self.notes.append(nextNote)
            noteDegree = (noteDegree + 2) % 7
            nextNote = self.mode[noteDegree]
        if rootDegree == 7:
            self.changeDegree(7, False)

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

    def transposeDown(self, steps):
        newChord = []
        for note in self.notes:
            for i in range(steps):
                newChord.append(note.flat())
        return newChord

    def minor(self):
        return self.changeDegree(4, False)
        # if 11 in noteIntervals:
        #   i = noteIntervals.index(11)
        #  self.notes[i].flat()

    def major(self):
        return self.changeDegree(3, True)
        # if 10 in noteIntervals:
        #   i = noteIntervals.index(11)
        #   self.notes[i].sharp()

    def sus2(self):
        self.changeDegree(4, False)
        self.changeDegree(3, False)
        # self.notes[1] = numToName[(root.toChromaticDegree + 2)]

    def sus4(self):
        self.changeDegree(4, True)
        self.changeDegree(3, True)

    # TODO
    # def addSeventh(self):
    #    self.notes.append()


c = Chord(1, 1, 5)  # C E G
# chordIII = chordI.transposeUp(4).minor() # E G B
# chordIV = chordI.transposeUp(5).major() # F A C
# chordV = chordI.transposeUp(7).major() # G B D
# chordVI = chordI.transposeUp(9).minor() # A C E


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
c.minor()
print c

