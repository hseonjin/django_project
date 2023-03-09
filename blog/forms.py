from socket import fromshare
from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        # fields 대신 exclude = ('post', 'author', 'created_at', 'modified_at')