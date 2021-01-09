from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment,Post


class CreateUserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','email','password1','password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=('author','title','text')

        widgets = {
            'title':forms.TextInput(attrs={'style':'color:black'}),
            'text':forms.Textarea(attrs={'style':'color:black'})
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author','text']

        widgets = {
            'author':forms.TextInput(attrs={'style':'color:black;'}),
            'text':forms.Textarea(attrs={'style':'color:black;'})
        }
