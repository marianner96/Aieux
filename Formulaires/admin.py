from django.contrib import admin

# Register your models here.

from Formulaires.models import Utilisateur, Famille

admin.site.register(Utilisateur)

admin.site.register(Famille)


