from django import forms

FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

class ExampleForm(forms.Form):
    favorite_color = forms.ChoiceField(choices=FAVORITE_COLORS_CHOICES)