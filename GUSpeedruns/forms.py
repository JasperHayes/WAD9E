from django import forms
from django.contrib.auth.models import User
from GUSpeedruns.models import Game, Comment, UserProfile

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
        
class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=50, help_text="Please enter a title.")
    content = forms.CharField(max_length=400, help_text="Please enter your comment.")
    
    class Meta: 
        model = Comment
        fields = ['title', 'content']
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)