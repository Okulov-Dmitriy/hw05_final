from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'image': ('Картинка в посте'),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
