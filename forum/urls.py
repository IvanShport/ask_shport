from django.conf.urls import url

from forum import views

urlpatterns = [
    url(r'^$', views.MainView, name='main'),
    url(r'^ask/$', views.AskView, name='ask'),
    url(r'^tag/(?P<pk>\d+)/$', views.TagView, name='tag'),
    url(r'^post/(?P<pk>\d+)/$', views.SingleView, name='single'),
    url(r'^post/(?P<pk>\d+)/like/$', views.LikeView, name='like'),
    url(r'^post/(?P<pk>\d+)/dislike/$', views.DislikeView, name='dislike'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.CommentView, name='comment'),
    url(r'^post/(?P<post_pk>\d+)/(?P<comment_pk>\d+)/like/$', views.CommentLikeView, name='commentlike'),
    url(r'^post/(?P<post_pk>\d+)/(?P<comment_pk>\d+)/dislike/$', views.CommentDislikeView, name='commentdislike'),
]
