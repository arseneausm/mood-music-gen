from django.shortcuts import render, redirect
from .forms import ExampleForm
from en.src.synthesize import synthesize
from django.conf import settings
from scipy.io import wavfile


# Create your views here.
def index(request):
	a = request.GET

	v = a['vibe']
	m = a['mood']
	s = a['spice']

	prog = synthesize(v, m, s)

	wavfile.write((settings.MEDIA_ROOT + '/player.wav'), 44100, prog)

	context = {
		'path' : settings.MEDIA_ROOT + 'player.wav'
	}

    # logic of view will be implemented here
	return render(request, "home.html", context)