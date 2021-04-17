import random

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
        self.noteNumber = Note.to_chromatic_degree(noteName)

    def __str__(self):
        return self.noteName

    @classmethod
    def to_chromatic_degree(cls, noteName):
        return nameToNum[noteName]

    def sharpen(self):
        self.noteNumber = (self.noteNumber + 1) % 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.noteName = notes[self.noteNumber]

    def sharp(self):
        i = (self.noteNumber + 1) % 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return notes[i]

    def flatten(self):
        self.noteNumber = (self.noteNumber - 1) % 12
        notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.noteName = notes[self.noteNumber]

    def flat(self):
        i = (self.noteNumber - 1) % 12
        notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        return notes[i]

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

    def change_degree(self, degree, sharp):
        noteIntervals = self.get_intervals_in_chord()
        if degree in noteIntervals:
            i = noteIntervals.index(degree)
            if sharp:
                self.notes[i].sharpen()
                return True
            else:
                self.notes[i].flatten()
                return True

    # ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    def __init__(self, mode, numNotes, rootDegree):
        # rootDegree indexed at 1 (for the sake of ii VI I etc)
        self.mode = mode
        noteDegree = rootDegree - 1
        self.root = self.mode[noteDegree]
        self.notes = []
        nextNote = self.mode[noteDegree]
        for i in range(numNotes):
            nextNote = self.mode[noteDegree]
            if nextNote not in self.notes:
                self.notes.append(nextNote)
            else:
                return
            noteDegree = (noteDegree + 2) % 7

    def copy_of(self, template):
        self.mode = template.mode
        self.root = template.root
        self.notes = template.notes

    def __str__(self):
        voicing = ''
        for note in self.notes:
            voicing = voicing + str(note) + ' '
        return voicing

    def add_note(self, noteToAdd):
        if noteToAdd not in self.notes:
            self.notes.append(noteToAdd)

    def get_intervals_in_chord(self):
        intervals = []
        for note in self.notes:
            intervals.append(Note.get_interval(self.root, note))
        return intervals

    def transpose_up(self, steps):
        newChord = []
        for note in self.notes:
            for i in range(steps):
                newChord.append(note.sharpen())
        return newChord

    def transpose_down(self, steps):
        newChord = []
        for note in self.notes:
            for i in range(steps):
                newChord.append(note.flatten())
        return newChord

    def major_minor_switch(self):
        if self.change_degree(3, True):
            self.change_degree(10, True)
            return
        if self.change_degree(4, False):
            self.change_degree(11, False)
            return

    def to_sus2(self):
        self.change_degree(4, False)
        self.change_degree(3, False)
        # self.notes[1] = numToName[(root.to_chromatic_degree + 2)]

    def to_sus4(self):
        self.change_degree(4, True)
        self.change_degree(3, True)


moodMod1Dict = {'happy': random.choice([majorModes[0], majorModes[1]]),
                }
moodMod2Dict = {'blue': [8,  # numChords
                         3   # degreeStart
                        ]
                }
moodMod3Dict = {'spicy': [[4, 5, 6],  # numNotesRange
                          0.75,  # chance for accidentals
                          5,  # weight for mode degrees
                          [2, 5, 6, 7]  # mode degrees to weight
                          ],
                'salt': [[2, 3],  # numNotesRange
                         0,  # chance for accidentals
                         0,  # weight for mode degrees
                         []  # mode degrees to weight
                         ],
                }


class Progression:

    def __init__(self,
                 moodMod1,
                 moodMod2,
                 moodMod3):
        self.chordSequence = []
        self.modeUsed = moodMod1Dict[moodMod1]
        self.numNotes = None
        self.numNotesRange = [3]
        weightedModeDegrees = [1, 1, 2, 3, 4, 5, 6, 7]
        self.degreeSequence = []

        self.numChords = moodMod2Dict[moodMod2][0]
        self.degreeSequence.append(moodMod2Dict[moodMod2][1])

        self.numNotesRange = moodMod3Dict[moodMod3][0]
        self.chanceForAccidentals = moodMod3Dict[moodMod3][1]
        self.weight = moodMod3Dict[moodMod3][2]
        self.degreesToWeight = moodMod3Dict[moodMod3][3]
        for i in range(self.weight):
            for d in range(len(self.degreesToWeight)):
                weightedModeDegrees.append(moodMod3Dict[moodMod3][3][d])

        # add new chord
        for i in range(self.numChords):
            self.chordSequence.append(self.gen_chord(self.degreeSequence[i]))
            self.degreeSequence.append(random.choice(weightedModeDegrees))

    def __str__(self):
        for chord in self.chordSequence:
            print str(chord)

    def gen_chord(self, degree):
        self.numNotes = random.choice(self.numNotesRange)
        chord = Chord(self.modeUsed, self.numNotes, degree)
        if random.random() <= self.chanceForAccidentals:
            chord.major_minor_switch()
        return chord

    # TODO
    # chords = an array of chords
    # change order of notes based on surrounding chords
    def voice_leading(self, chords):
        self.chords = []
        for i in (range(len(chords)) - 1):
            self.chords.append(chords[i].voiced(i + 1))
        pass


# c1 = Chord(1, 4, 2)  # D F A C
# c2 = Chord(1, 4, 5)  # G B D F
# c3 = Chord(1, 4, 1)  # C E G B
# print c1
# print c2
# print c3

# rootChord = Chord(1, 1, 1)
# rootChord.copy_of(c3)
# print rootChord
# tempChord = Chord(1, 3, 1)

moodMod1 = 'happy'
moodMod2 = 'blue'
moodMod3 = 'spicy'

testProgression = Progression(moodMod1, moodMod2, moodMod3)