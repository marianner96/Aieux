from django.conf.urls import include,url
from django.contrib import admin

from Formulaires import views


app_name = 'Formulaires'
urlpatterns = [
    url(r'^$', views.accueilForm, name='accueilForm'),
    url(r'^admin/$', admin.site.urls),
    url(r'^InscriptionForm/$', views.InscriptionForm, name='InscriptionForm'),
    url(r'^modificationForm/$', views.modificationForm, name='modificationForm'),
    url(r'^Menubis/$', views.Menubis, name='Menubis'),
    url(r'^Menu/$', views.Menu, name='Menu'),
    url(r'^Form_famille/$', views.Form_famille, name='Form_famille'),
    url(r'^Form_event/$', views.Form_event, name='Form_event'),

    url(r'^arbre/$',views.arbre,name='arbre'),
    url(r'^add_membre_arbre/$',views.add_membre_arbre,name='add_memebre_arbre'),

    url(r'^supp_membre_arbre/$',views.supp_membre_arbre,name='supp_memebre_arbre'),

    url(r'^maj_arbre/$',views.maj_arbre,name='maj_arbre'),
    url(r'^modifierfichier/$',views.modifierfichier,name='modifierfichier'),
    url(r'^maj_lsc/$',views.maj_lsc,name='maj_lsc'),

    url(r'^maj_lnp/$',views.maj_lnp,name='maj_lnp'),
    url(r'^maj_np/$',views.maj_np,name='maj_np'),
    url(r'^maj_np2/$',views.maj_np2,name='maj_np2'),

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

<<<<<<< HEAD
    url(r'^sendmail/$', views.sendmail, name='sendmail'),
    url(r'^Envoi_Email/$', views.Envoi_Email, name='Envoi_Email'),
    url(r'^renvoi_Email/$', views.renvoi_Email, name='renvoi_Email'),
=======
    url(r'^supprime_membre/$',views.supprime_membre,name='supprime_membre'),
    url(r'^initialise_fichier/$',views.initialise_fichier,name='initialise_fichier')
>>>>>>> 111744818e92bf81337bedd5fb31bdb1bd107b86
]

#l'admin a pour nom eisti et le mdp est rogerdeeisti

#Autre admin : 
#Username : eisti
#adresse : eisti@eisti.eu
#mdp : aieuxaieux