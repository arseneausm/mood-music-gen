import numpy as np
from scipy.io import wavfile

# Returns the frequency of the nth key
def key_freq(n):
    return (2**(1 / 12))**(n - 49) * 440 # Hz

def note_freq(octave, note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] 

    if octave == 0:
        notes = ['A', 'A#', 'B']

        if note in notes:
            freq = key_freq(notes.index(note) + 1)
            return freq
        else:
            print('Err: Note not in octave!')
            return 0

    elif octave == 8:
        notes = ['C']

        if note in notes:
            freq = key_freq(88)
            return freq
        else:
            print('Err: Note not in octave!')
            return 0

    else:
        if note in notes:
            n = 12 * (octave - 1) + notes.index(note) + 4
            freq = key_freq(n)
            return freq
        else:
            print('Err: Note not in octave!')
            return 0

def get_adsr_weights(frequency, duration, length, decay, sustain_level, sample_rate=44100):

    assert abs(sum(length)-1) < 1e-8
    assert len(length) ==len(decay) == 4
    
    intervals = int(duration*frequency)
    len_A = np.maximum(int(intervals*length[0]),1)
    len_D = np.maximum(int(intervals*length[1]),1)
    len_S = np.maximum(int(intervals*length[2]),1)
    len_R = np.maximum(int(intervals*length[3]),1)
    
    decay_A = decay[0]
    decay_D = decay[1]
    decay_S = decay[2]
    decay_R = decay[3]
    
    A = 1/np.array([(1-decay_A)**n for n in range(len_A)])
    A = A/np.nanmax(A)
    D = np.array([(1-decay_D)**n for n in range(len_D)])
    D = D*(1-sustain_level)+sustain_level
    S = np.array([(1-decay_S)**n for n in range(len_S)])
    S = S*sustain_level
    R = np.array([(1-decay_R)**n for n in range(len_R)])
    R = R*S[-1]
    
    weights = np.concatenate((A,D,S,R))
    smoothing = np.array([0.1*(1-0.1)**n for n in range(5)])
    smoothing = smoothing/np.nansum(smoothing)
    weights = np.convolve(weights, smoothing, mode='same')
    
    weights = np.repeat(weights, int(sample_rate*duration/intervals))
    tail = int(sample_rate*duration-weights.shape[0])
    if tail > 0:
        weights = np.concatenate((weights, weights[-1]-weights[-1]/tail*np.arange(tail)))
    return weights

def get_note(octave, note, duration = 0, beats = 0, bpm = 0, sample_rate=44100, amplitude=4096, save = False):
    if duration == 0:
        duration = beats * (60 / bpm)

    frequency = note_freq(octave, note)
    freqs = []
    amps = []

    fund = 7

    for n in range(1,fund):
        freqs.append((n + 1) * frequency)
        amps.append((0.5)**n * amplitude)

    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    wave = amplitude*np.sin(2*np.pi*frequency*t)

    for i in range(len(freqs)):
        wave += amps[i]*np.sin(2*np.pi*freqs[i]*t)

    if save:
        wavfile.write(('' + str(note) + str(octave) + '.wav'), rate=44100, data=wave.astype(np.int16))

    return wave, frequency

def piano(octave, note, duration, lens = [0.05, 0.25, 0.55, 0.15], save = False):
    note, f = get_note(octave, note, duration, save = save)

    weights = get_adsr_weights(f, duration, lens, 
    return note

octave = int(input('Octave: '))
note = str(input('Note: '))
duration = int(input('Duration: '))

w1 = piano(octave, note, duration, save = True)
w2 = get_note(4, 'G', 4, save = True)

fin = w1 + w2

wavfile.write('firstchord.wav', rate=44100, data=fin.astype(np.int16))
