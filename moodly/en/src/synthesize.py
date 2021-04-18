from scipy.io import wavfile

from . import progression_producer
from . import synth
import numpy as np

from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static


def synthesize(v, m, s):
    vibe = v
    mood = m
    spice = s

    output = progression_producer.Progression(vibe, mood, spice)
    print(output)

    octave = 4
    duration = 20
    chordDuration = duration / len(output.chordSequence)
    synthChords = np.zeros((int(chordDuration * 44100)))

    chords = []

    for chord in output.chordSequence:
        synthNotesList = []
        for note in chord.notes:
            noteName = note.noteName
            synthNote = synth.Note(noteName, octave, chordDuration)
            synthNotesList.append(synthNote)

        print(len(synthNotesList))
        chords.append(synth.Chord(synthNotesList))

    print(len(chords))

    progression = np.array([])

    for i in range(len(chords)):
        progression = np.append(progression, chords[i].wav)

    #wavfile.write('', rate=44100, data=progression.astype(np.int16))

    return progression


# synthesize_progression('ihop-commercial', 'beige', 'salt')