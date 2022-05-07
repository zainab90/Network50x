from django import forms
from network.models import Post, Comment, Follower, User


class PostForm(forms.ModelForm):
    post_body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'3', 'placeholder':'Enter'}),label='Enter your Post')
    class Meta:
        model = Post
        fields = [
            'post_body'
        ]

