from django.shortcuts import get_object_or_404, render
import datetime
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from forum.models import list_of_tags, main_manager, tag_manager, Post, LikePost, LikeComment, Comment
from forum.forms import AskForm
from authorization.models import Profile


def MainView(request):
    context = main_manager(request)

    return render(request, "forum/main.html", context)


@login_required
def AskView(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form.save(request)
            url = request.POST.get('next', '/')
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, "forum/ask.html", {
        'form': form})


def TagView(request, pk):
    context = tag_manager(request, pk)
    return render(request, "forum/main.html", context)


def SingleView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, "forum/single.html", {
        'post': post,
    })


@login_required
def CommentView(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.views -= 1
        post.save()
        text = request.POST.get('text')
        if (text == ''):
            return HttpResponseRedirect(reverse('forum:single', args=(pk,)))
        comment = Comment()
        comment.post = post
        comment.text = text
        comment.author = get_object_or_404(Profile, user=request.user)
        comment.number = str(comment.post.comment_set.all().count() + 1)
        comment.save()
    return HttpResponseRedirect(reverse('forum:single', args=(pk,)))


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = get_object_or_404(Profile, user=request.user)
    likes = LikePost.objects.filter(post=pk).filter(user=current_user)

    if likes.count() > 0:
        if likes[0].value == 1:
            likes.delete()
        elif likes[0].value == -1:
            likes[0].value = 1
            likes[0].save()
    else:
        post.likepost_set.create(user=current_user, value=1)
    post.views -= 1
    post.save()
    return HttpResponseRedirect(reverse('forum:single', args=(pk,)))


@login_required
def DislikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = get_object_or_404(Profile, user=request.user)
    likes = LikePost.objects.filter(post=pk).filter(user=current_user)
    if likes.count() > 0:
        if likes[0].value == -1:
            likes.delete()
        elif likes[0].value == 1:
            likes[0].value = -1
            likes[0].save()
    else:
        post.likepost_set.create(user=current_user, value=-1)
    post.views -= 1
    post.save()
    return HttpResponseRedirect(reverse('forum:single', args=(pk,)))


@login_required
def CommentLikeView(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    current_user = get_object_or_404(Profile, user=request.user)
    likes = LikeComment.objects.filter(comment=comment_pk).filter(user=current_user)
    if likes.count() > 0:
        if likes[0].value == 1:
            likes.delete()
        elif likes[0].value == -1:
            likes[0].value = 1
            likes[0].save()
    else:
        comment.likecomment_set.create(user=current_user, value=1)
    post.views -= 1
    post.save()
    return HttpResponseRedirect(reverse('forum:single', args=(post_pk,)))


@login_required
def CommentDislikeView(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    current_user = get_object_or_404(Profile, user=request.user)
    likes = LikeComment.objects.filter(comment=comment_pk).filter(user=current_user)
    if likes.count() > 0:
        if likes[0].value == -1:
            likes.delete()
        elif likes[0].value == 1:
            likes[0].value = -1
            likes[0].save()
    else:
        comment.likecomment_set.create(user=current_user, value=-1)
    post.views -= 1
    post.save()
    return HttpResponseRedirect(reverse('forum:single', args=(post_pk,)))
