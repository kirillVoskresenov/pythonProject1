from django import forms
from .models import Post

class PostsForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'post_type',
           'title',
           'category',
           'text'
       ]

