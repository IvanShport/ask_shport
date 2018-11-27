from django.conf.urls import url

from authorization import views

urlpatterns = [
    url(r'^$', views.LoginView, name='login'),
    url(r'^logout/$', views.LogoutView, name='logout'),
    url(r'^registration/$', views.RegistrationView, name='registration'),
    url(r'^settings/$', views.SettingsView, name='settings'),
]
