from django import forms
from django.contrib.auth.models import User
from GUSpeedruns.models import Game, Comment, UserProfile, Run

        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class UploadGameForm(forms.ModelForm):
    name = forms.CharField(max_length=Game.NAME_MAX_LENGTH, help_text="Please enter the game name:")
    image = forms.ImageField(required=False, help_text="Upload image (optional):")
    date_released = forms.DateField( help_text="Please enter the game's release date:", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Game
        fields = ("name", "image", "date_released")

class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=Comment.TITLE_MAX_LENGTH, help_text="Please enter a title", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter a title for your comment','id': 'title'}))                                                                                                                 
    content = forms.CharField(max_length=Comment.CONTENT_MAX_LENGTH, help_text="Please enter your comment:", widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write your comment here','id': 'content', 'rows':8}))
    
    class Meta: 
        model = Comment
        fields = ['title', 'content']



class RunForm(forms.ModelForm):
    video = forms.URLField(max_length= 200, help_text= "Youtube link:")
    hours = forms.IntegerField(min_value=0, help_text="Time - Hr:")
    minutes = forms.IntegerField(min_value=0, max_value=59, help_text= "Min:")
    seconds = forms.IntegerField(min_value=0, max_value=59, help_text="Sec:")
    milliseconds = forms.IntegerField(min_value=0, max_value=999, help_text="Ms:")
    description = forms.CharField(max_length=Run.DESCRIPTION_MAX_LENGTH, help_text= "Description:")

    class Meta:
        model = Run
        fields = ('video', 'description', 'hours', 'minutes', 'seconds', 'milliseconds')