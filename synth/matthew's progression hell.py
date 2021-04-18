# okay so here we go

# basic scale array -- pretending everything is in Cmaj
# gonna build it with scale degree VARIABLES
# but they're gonna redirect to the semitone scale degree/distance from root note...
# i.e. scale degree 'C' = 0, scale degree 'D' = 2, 'E' = 4 (major third), etc
C = 0
D = 2
E = 4
F = 5
G = 7
A = 9
B = 11
C2 = 12


def sharpen(note):
    return note+1


def flatten(note):
    return note-1

majorScale = [C, D, E, F, G, A, B, C2]
minorScale = [C, D, flatten(E), F, G, flatten(A), flatten(B), C2]



