from django.conf.urls import url

from . import views

app_name = 'Formulaires'
urlpatterns = [
    url(r'^$', views.accueilForm, name='accueilForm'),
    url(r'^inscriptionForm/$', views.inscriptionForm, name='inscriptionForm'),
    url(r'^connectionForm/$', views.connectionForm, name='connectionForm'),
    url(r'^modificationForm/$', views.modificationForm, name='modificationForm'),
    url(r'^Felicitations/$', views.Felicitations, name='Felicitations'),
]

