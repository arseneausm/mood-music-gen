from django.db import models

# Create your models here.

class Vibe(models.Model):
	vibe = models.Charfield(max_length=40)

	def __str__(self):
		return self.vibe

class Mood(models.Model):
	mood = models.Charfield(max_length=40)

	def __str__(self):
		return self.mood

class Spice(models.Model):
	spice = models.Charfield(max_length=40)

	def __str__(self):
		return self.spice
		