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

    def __eq__(self, other):
        return self.noteNumber == other.noteNumber

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
        return Note(notes[i])

    def flatten(self):
        self.noteNumber = (self.noteNumber - 1) % 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.noteName = notes[self.noteNumber]

    def flat(self):
        i = (self.noteNumber - 1) % 12
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return Note(notes[i])

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
                self.notes[i] = self.notes[i].sharp()
                return True
            else:
                self.notes[i] = self.notes[i].flat()
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
            if numNotes == 2:
                noteDegree = (noteDegree + 4) % 7
            else:
                noteDegree = (noteDegree + 2) % 7

    def set_notes(self, notes):
        self.notes = notes

    def copy_of(self, template):
        self.mode = template.mode
        self.root = template.root
        self.notes = template.notes

    def __str__(self):
        voicing = ''
        for note in self.notes:
            voicing = voicing + str(note) + ' '
        return voicing

    def __eq__(self, other):
        for i in range(3):
            if self.notes[i] != other.notes[i]:
                return False
        return True

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


def voiceChord(currentChord, lastChord):
    voicedChord = []
    destNotes = currentChord.notes
    sourceNotes = lastChord.notes
    i = 0
    matrix = []
    for s_note in sourceNotes:
        v = []
        for d_note in destNotes:
            min_distance = min(abs(d_note.noteNumber - s_note.noteNumber), 12 - abs(d_note.noteNumber - s_note.noteNumber))
            v.append(min_distance)
        matrix.append(v)
    # print matrix
    mapMinDict = {}
    for j in range(len(matrix[0])):
        standing_min = 12
        min_index = -1
        for i in range(len(matrix)):
            if matrix[i][j] < standing_min:
                min_index = i
                standing_min = matrix[i][j]
                # TODO if matrix[i][j] == standing_min, add to an array of min_indexes
        mapMinDict[j] = min_index
    # print mapMinDict
    voicedChordRef = mapMinDict.items()
    voicedChordRef = sorted(voicedChordRef, key = lambda x: x[1])
    voicedChordRef = [x[0] for x in voicedChordRef]
    # print voicedChordRef
    for num in voicedChordRef:
        note = destNotes[num]
        voicedChord.append(note)
    return voicedChord  # returns an array of notes, to use, eg c2.set_notes(voiceChord(c2, c1))


vibeDict = {  # vibe -- target at night, summer breeze (lydian),
    # ihop commercial (ionian), smoky jazz lounge (mixolydian),
    # sunglasses and a mustache (dorian), ancient ritual (phrygian), demon palace DO NOT TOUCH! (locrian)
    # eating ice cream in the shower (aoleian)
    'ihop commercial':
        modes[1],

    'sunglasses and a mustache':  # dorian
        modes[2],

    'ancient ritual':  # phrygian
        modes[3],

    'summer breeze':
        modes[4],

    'smoky jazz lounge':  # mixo
        modes[5],

    'eating ice cream in the shower':
        modes[6],

    'denny\'s at 2am':     # locrian
        modes[7],

}

moodDict = {  # mood
    # porcelain, beige, marigold, cherry, mahogany, bubblegum, boysenberry, sapphire, chartreuse, onyx
    'porcelain':
        [4,  # numChords
         4,  # degreeStart
         4,  # weight for mode degrees
         [4, 5, 5, 6, 1, 4, 1]  # mode degrees to weight
         ],
    'beige':
        [2,  # numChords
         2,  # degreeStart
         6,  # weight for mode degrees
         [1, 2, 5, 1, 1]  # mode degrees to weight
         ],
    'marigold':
        [6,  # numChords
         3,  # degreeStart
         2,  # weight for mode degrees
         [3, 3, 6, 5, 1]  # mode degrees to weight
         ],
    'cherry':
        [4,  # numChords
         1,  # degreeStart
         6,  # weight for mode degrees
         [1, 1, 5, 5, 1, 5, 4, 5, 4]  # mode degrees to weight
         ],
    'mahogany':
        [5,  # numChords
         2,  # degreeStart
         2,  # weight for mode degrees
         [1, 1, 5, 5, 1, 5, 2, 5, 2, 2, 2, 2, 7]  # mode degrees to weight
         ],
    'bubblegum':
        [8,  # numChords
         1,  # degreeStart
         10,  # weight for mode degrees
         [1, 1, 5, 5, 1, 5, 5, 4]  # mode degrees to weight
         ],
    'boysenberry':
        [3,  # numChords
         6,  # degreeStart
         6,  # weight for mode degrees
         [5, 4, 1, 3, 2, 1, 6, 5, 6]  # mode degrees to weight
         ],
    'sapphire':
        [5,  # numChords
         4,  # degreeStart
         8,  # weight for mode degrees
         [4, 4, 1, 1, 1, 1, 4, 5, 4]  # mode degrees to weight
         ],
    'chartreuse':
        [5,  # numChords
         3,  # degreeStart
         5,  # weight for mode degrees
         [1, 3, 4, 5, 1, 1, 4, 5, 6]  # mode degrees to weight
         ],
    'onyx':
        [6,  # numChords
         7,  # degreeStart
         1,  # weight for mode degrees
         [6, 4, 2, 2, 2, 1, 7, 5, 4]  # mode degrees to weight
         ]
}

spiceDict = {  # spice
    # chili powder, garam masala, ginger, cinnamon, pepper, coriander, msg, paprika, salt, oregano, saffron, sugar
    'sugar':
        [[2, 3, 3, 4, 4],  # numNotesRange
         0.08  # chance for accidentals
         ],
    'saffron':
        [[2, 3, 3, 3, 4],  # numNotesRange
         0.16  # chance for accidentals
         ],
    'oregano':
        [[2, 3, 3, 3, 4, 5],  # numNotesRange
         0.24  # chance for accidentals
         ],
    'salt':
        [[3, 3, 3, 4, 4],  # numNotesRange
         0.32  # chance for accidentals
         ],
    'paprika':
        [[2, 3, 4, 4, 4, 5],  # numNotesRange
         0.40  # chance for accidentals
         ],
    'msg':
        [[4, 3],  # numNotesRange
         0.48  # chance for accidentals
         ],
    'coriander':
        [[3, 4, 5],  # numNotesRange
         0.56  # chance for accidentals
         ],
    'pepper':
        [[3, 3, 4, 5, 6],  # weighted numNotesRange
         0.64  # chance for accidentals
         ],
    'cinnamon':
        [[3, 4, 4, 6, 5],  # numNotesRange
         0.72  # chance for accidentals
         ],
    'ginger':
        [[3, 4, 4, 5, 5],  # numNotesRange
         0.8  # chance for accidentals
         ],
    'garam masala':
        [[3, 4, 4, 4, 5, 6, 6, 7],  # numNotesRange
         0.88  # chance for accidentals
         ],
    'chili powder':
        [[4, 4, 5, 5, 5, 6, 7],  # numNotesRange
         0.96  # chance for accidentals
         ]
    # coriander, saffron, paprika, oregano, msg, cinnamon, garam masala,
    # chili powder, garam masala, ginger, cinnamon, pepper, coriander, msg, paprika, salt, oregano, saffron, sugar
}


class Progression:

    def __init__(self,
                 mood_mod1,
                 mood_mod2,
                 mood_mod3):
        self.chordSequence = []
        self.modeUsed = vibeDict[mood_mod1]
        self.numNotes = None
        self.numNotesRange = [3]
        weightedModeDegrees = [1, 1, 2, 3, 4, 5, 6, 7]
        self.degreeSequence = []

        self.numChords = moodDict[mood_mod2][0]
        self.degreeSequence.append(moodDict[mood_mod2][1])

        self.numNotesRange = spiceDict[mood_mod3][0]
        self.chanceForAccidentals = spiceDict[mood_mod3][1]
        self.weight = moodDict[mood_mod2][2]
        self.degreesToWeight = moodDict[mood_mod2][3]
        for i in range(self.weight):
            for d in range(len(self.degreesToWeight)):
                weightedModeDegrees.append(moodDict[mood_mod2][3][d])

        # add new chord
        lastChord = self.gen_chord(self.degreeSequence[0])
        i = 0
        while i <= self.numChords:
            nextChord = self.gen_chord(self.degreeSequence[i])
            if not nextChord == lastChord:
                self.chordSequence.append(nextChord)
                lastChord = nextChord
                i = i + 1
            self.degreeSequence.append(random.choice(weightedModeDegrees))
        self.voice_all()

    def __str__(self):
        chords = ''
        for chord in self.chordSequence:
            chords = chords + str(chord) + '\n'
        return chords

    def gen_chord(self, degree):
        sharpenNote = True
        self.numNotes = random.choice(self.numNotesRange)
        chord = Chord(self.modeUsed, self.numNotes, degree)
        copyChord = Chord(self.modeUsed, 1, 1)
        copyChord.copy_of(chord)
        if random.random() <= self.chanceForAccidentals:
            degreeToChange = random.choice([4, 3, 9, 8, 10, 11])
            if degreeToChange == 4 or degreeToChange == 9 or degreeToChange == 11:
                sharpenNote = False
            else:
                degreeToChange = random.choice([3, 8, 10])
            copyChord.change_degree(degreeToChange, sharpenNote)
            # chord.change_degree(degreeToChange, not sharpenNote)
        # print 11 in copyChord.get_intervals_in_chord()

        return copyChord

    # TODO
    # chords = an array of chords
    # change order of notes based on surrounding chords
    def voice_all(self):
        i = 1
        while i < len(self.chordSequence):
            currentChord = self.chordSequence[i]
            lastChord = self.chordSequence[i-1]
            currentChord.set_notes(voiceChord(currentChord, lastChord))
            i = i + 1

    # c2.set_notes(voiceChord(c2, c1))

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

#vibe1 = random.choice(vibeDict.keys())  # 'ihop commercial'
#mood1 = random.choice(moodDict.keys())  # 'porcelain'
#spice1 = random.choice(spiceDict.keys())  # 'chili powder'

#testProgression = Progression(vibe1, mood1, spice1)
#print "Here's a little something inspired by a " + mood1 + " " + vibe1 + " with " + spice1 + ".\n"
#print testProgression