from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from forum.models import list_of_tags, Post
from authorization.models import Profile

class AskForm(forms.Form):
    title = forms.CharField(max_length=64)
    text = forms.CharField(widget=forms.Textarea)
    tag = forms.CharField(max_length=64)

    def save(self, request):
        post = Post()
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.author = get_object_or_404(Profile, user=request.user)
        post.pub_date = timezone.now()
        tag = self.cleaned_data['tag']
        post.save()
        list_of_tags(post, tag)
        post.save()

        return post