# mood-music-gen
Engine for generating chord progressions, developed for HackDartmouth 2021.

## Todo:
Solve the WAV saving equation. Will have to research how WAV files are stored but the basic premise is:

1. Craft a WAV header
2. Figure out what the data of a WAV file looks like
3. Output an appropriate hexdump that could be a wav file to a string
4. Save the string as a .wav using django

Alternatively (might be easier considerably):

Rewrite the webapp in JS and see if that'll help it.

https://en.wikipedia.org/wiki/WAV
