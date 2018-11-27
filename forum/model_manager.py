from django.db import models
from django.utils import timezone

class PostManager(models.Manager):
    def get_new(self):
        return self.get_queryset().filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    def get_new_tag(self, pk):
        return self.get_queryset().filter(tags__pk=pk, pub_date__lte=timezone.now()).order_by('-pub_date')

    def get_popular(self):
        return self.get_queryset().filter(pub_date__lte=timezone.now()).order_by('-views')

    def get_popular_tag(self, pk):
        return self.get_queryset().filter(tags__pk=pk, pub_date__lte=timezone.now()).order_by('-views')

    def get_favourite(self):
        return self.get_queryset().filter(pub_date__lte=timezone.now()).order_by('-like')

    def get_favourite_tag(self, pk):
        return self.get_queryset().filter(tags__pk=pk, pub_date__lte=timezone.now()).order_by('-like')

