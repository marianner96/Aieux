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

    url(r'^initialise_fichier/$',views.initialise_fichier,name='initialise_fichier'),
    url(r'^arbre/$',views.arbre,name='arbre'),
    url(r'^add_membre_arbre/$',views.add_membre_arbre,name='add_memebre_arbre'),
    url(r'^modifierfichier/$',views.modifierfichier,name='modifierfichier'),
    url(r'^maj_lsc/$',views.maj_lsc,name='maj_lsc'),
    url(r'^maj_lsc_b/$',views.maj_lsc_b,name='maj_lsc_b'),
    url(r'^maj_lnp/$',views.maj_lnp,name='maj_lnp'),
    url(r'^maj_le_parametre/$',views.maj_le_parametre,name='maj_le_parametre'),
    url(r'^add_enfant/$',views.add_enfant,name='add_enfant'),
    url(r'^add_couple/$',views.add_couple,name='add_couple'),
    url(r'^supp_lsc/$',views.supp_lsc,name='supp_lsc'),
    url(r'^supp_le/$',views.supp_le,name='supp_le'),
    url(r'^maj_lnc/$',views.maj_lnc,name='maj_lnc'),
    url(r'^supp_les/$',views.supp_les,name='supp_les'),
    url(r'^maj_nodes_edges/$',views.maj_nodes_edges,name='maj_nodes_edges'),
    url(r'^maj_enfant/$',views.maj_enfant,name='maj_enfant'),
    url(r'^maj_parent/$',views.maj_parent,name='maj_parent'),
    url(r'^maj_couple/$',views.maj_couple,name='maj_couple'),

]

