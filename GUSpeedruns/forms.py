from django import forms
from GUSpeedruns.models import Game

class UploadGameForm(forms.ModelForm):
    name = forms.CharField(max_length=Game.NAME_MAX_LENGTH, help_text="Please enter the game name.")

    class Meta:
        model = Game
        fields = ("name", "image", "date_released")

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter game name'
            }),
            'date_released': forms.DateInput(attrs={
                'type': 'date'
            })
        }