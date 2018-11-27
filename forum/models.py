import datetime

from django.db import models, IntegrityError
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.models import User
from authorization.models import Profile
from forum.model_manager import PostManager
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def main_manager(request):
    if request.GET.get('sort', 'date') == 'rating':
        posts = Post.get_posts.get_favourite()
        title = 'Понравившиеся вопросы'
    elif request.GET.get('sort', 'date') == 'views':
        posts = Post.get_posts.get_popular()
        title = 'Популярные вопросы'
    else:
        posts = Post.get_posts.get_new()
        title = 'Новые вопросы'

    page, paginator, before_list, after_list = my_paginator(request, posts)

    return {'page': page,
            'paginator': paginator,
            'before_list': before_list,
            'after_list': after_list,
            'title': title,
            }

def tag_manager(request, pk):
    if request.GET.get('sort', 'date') == 'rating':
        post = Post.get_posts.get_favourite_tag(pk)
    elif request.GET.get('sort', 'date') == 'views':
        post = Post.get_posts.get_popular_tag(pk)
    else:
        post = Post.get_posts.get_new_tag(pk)

    page, paginator, before_list, after_list = my_paginator(request, post)

    return {'page': page,
            'paginator': paginator,
            'before_list': before_list,
            'after_list': after_list,
            'tag': Tag.objects.get(pk=pk).title,
            'title': 'Тег: ',
            }

def my_paginator(request, data):
    limit = 1

    page = request.GET.get('page', 1)
    paginator = Paginator(data, limit)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    before_list = []
    for i in range(5):
        if page.number > i + 1:
            before_list.append(page.number - i - 1)
    before_list.reverse()
    after_list = []
    for i in range(5):
        if page.number < paginator.num_pages - i:
            after_list.append(page.number + i + 1)

    return page, paginator, before_list, after_list

def list_of_tags(post, tags):
    list_tags = str(tags).split(', ')
    for tag in list_tags:
        try:
            post.tags.create(title = tag)
        except IntegrityError:
            post.tags.add(Tag.objects.get(title = tag))

class Tag(models.Model):
    title = models.CharField(max_length = 32, unique=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    views = models.IntegerField(default=0)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=64)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    get_posts = PostManager()

    def get_likes(self):
        return self.likepost_set.filter(value = 1).count()

    def get_dislikes(self):
        return self.likepost_set.filter(value = -1).count()

    def __str__(self):
        return self.title

class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1024)
    pub_date = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length = 32)

    def get_rating(self):
        likes = self.likecomment_set.filter(value = 1).count()
        dislikes = self.likecomment_set.filter(value = -1).count()
        return likes - dislikes

    def __str__(self):
        return self.number

class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)
