from django.conf.urls import url
from django.contrib import admin

from Formulaires import views


app_name = 'Formulaires'
urlpatterns = [
    url(r'^$', views.accueilForm, name='accueilForm'),
    url(r'^admin/', admin.site.urls),
    url(r'^InscriptionForm/$', views.InscriptionForm, name='InscriptionForm'),
    url(r'^modificationForm/$', views.modificationForm, name='modificationForm'),
    url(r'^Felicitations/$', views.Felicitations, name='Felicitations'),
    url(r'^Menubis/$', views.Menubis, name='Menubis'),
    url(r'^Menu/$', views.Menu, name='Menu'),
    url(r'^Form_famille/$', views.Form_famille, name='Form_famille'),
    url(r'^Rejoindre_famille/$', views.Rejoindre_famille, name='Rejoindre_famille'),
    url(r'^Form_famille_ajoutmembre/$', views.Form_famille_ajoutmembre, name='Form_famille_ajoutmembre'),
    url(r'^Form_event/$', views.Form_event, name='Form_event'),
    url(r'^Confirm_ajoutevent/$', views.Confirm_ajoutevent, name='Confirm_ajoutevent'),
    url(r'^logout/$', views.logout_view, name='logout'),
]

