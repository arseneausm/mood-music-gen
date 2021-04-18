from scipy.io import wavfile

import progression_producer
import synth
import numpy as np

vibe = 'ihop commercial'  # raw_input("Pick a vibe\n")
# print ("You picked: " + vibe)
mood = 'mahogany'  # raw_input("Pick a mood\n")
spice = 'salt'  # raw_input("Pick a spice\n")

output = progression_producer.Progression(vibe, mood, spice)
print(output)

octave = 4
duration = 100
chordDuration = duration / len(output.chordSequence)
synthChords = np.zeros(((chordDuration * 44100)))


for chord in output.chordSequence:
    synthNotesList = []
    for note in chord.notes:
        noteName = note.noteName
        synthNote = synth.Note(noteName, octave, chordDuration)
        synthNotesList.append(synthNote)
    np.append(synthChords, synth.Chord(synthNotesList).wav)
    # synthChords = synthChords + synth.Chord(synthNotesList).wav

wavfile.write('synthChords.wav', rate=44100, data=synthChords.astype(np.int16))

