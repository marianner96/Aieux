#!/usr/bin/python
# -*- coding:Utf-8 -*-

##################
## Author : Léa
## Name : Formulaire.py
###################

import cgitb
cgitb.enable()
import cgi
import urllib2

print "Content-Type: text/html\n" 

print """<!DOCTYPE html>

<html>
    <head>
        <meta charset=\"UTF-8">
        <title>Une page Web</title>
    </head>

    <body>"""

def inscription():
	print ("<div id=\"inscription\">")
	print ("<form class=\"form-horizontal\" name=\"formu\" role=\"form\" action=\"javascript:confirm_inscription()\">")
	print ("<label for=\"nom\">Nom : </label>")
	print ("<input type=\"nom\" class=\"form-control\" required=\"required\" id=\"nom_inscr\"></input><br/>")
	print ("<label for=\"prenom\">Prénom : </label>")
	print ("<input type=\"prenom\" class=\"form-control\" required=\"required\" id=\"prenom_inscr\"></input><br/>")
	print ("<label>Genre : <input type=\"radio\" id=\"genre_inscr\" value=\"masculin\"> Masculin <input type=\"radio\" id=\"genre_inscr\" value=\"féminin\"> Féminin</label><br/>")
	print ("<label for=\"ddn\">Date de naissance : </label>")
	print ("<input type=\"date\" class=\"form-control\" required=\"required\" id=\"ddn_inscr\"></input><br/>")
	print ("<label for=\"email\">E-mail : </label>")
	print ("<input type=\"email\" class=\"form-control\" required=\"required\" id=\"email_inscr\"></input><br/>")
	print ("<label for=\"mdp\">Mot de passe : </label>")
	print ("<input type=\"password\" class=\"form-control\" required=\"required\" id=\"mdp_inscr\"></input><br/>")
	print ("<br/>")
	print ("<div><button type=\"submit\" id=\"bouton\" class=\"btn btn-primary\">Valider</button></div>")
	print ("</form>")
	print ("</div>")

def modif():
	print ("<form id=\"modif\">")
	print ("<div id=\"img\">")
	print ("<label><input type=\"image\" name=\"img_modif\" src=\"../images/profil_chat.jpg\" width=\"200\" height=\"auto\"></label></div>")
	print ("<input type=\"button\" onclick=\"javascript:changerimg()\" value=\"Changer la photo\"><br/><br/>")
	print ("<label>Nom : <input type=\"text\" name=\"nom_modif\" value=\"nom qu'il y a dans la BDD\" required autofocus></label><br/><br/>")
	print ("<label>Prénom : <input type=\"text\" name=\"prenom_modif\" value=\"prénom qu'il y a dans la BDD\" required autofocus></label><br/>")
	print ("<label>Autre prénoms : <input type=\"text\" name=\"autrepren_modif\" value=\"autres prénoms qu'il y a dans la BDD\" autofocus></label><br/>")
	print ("<!--Pour le genre il faut regarder ce qui est coché dans la BDD...-->")
	print ("<label>Genre : <input type=\"radio\" name=\"genre_modif\" value=\"masculin\"> Masculin <input type=\"radio\" name=\"genre_modif\" value=\"féminin\"> Féminin </label><br/>")
	print ("<!--Marche pas sur Firefox-->")
	print ("<label>Date de naissance : <input type=\"date\" name=\"ddn_modif\"  value=\"ddn qu'il y a dans la BDD\" required autofocus></label><br/>")
	print ("<label>Mot de passe : <input type=\"password\" name=\"mdp_modif\" required autofocus></label><br/>")
	print ("<label>Adresse e-mail : <input type=\"email\" name=\"email_modif\"  value=\"email qu'il y a dans la BDD\" required autofocus></label><br/>")
	print ("<label>Adresse postale : <input type=\"text\" name=\"postal_modif\" value=\"adresse qu'il y a dans la BDD\" autofocus></label><br/>")
	print("<label>Profession : <input type=\"text\" name=\"profession_modif\" value=\"profession qu'il y a dans la BDD\" autofocus></label><br/>")
	print ("<label>Description : <input type=\"textarea\" name=\"descr_modif\" value=\"description qu'il y a dans la BDD\" autofocus></label><br/>")
	print ("</form>")
	print ("<input type=\"button\" name=\"btn\" value=\"Modifier\">")

def connec():
	print ("<form id=\"connec\"> <label>Adresse e-mail : <input type=\"email\" name=\"email_connec\" required></label><br/>")
	print ("<label>Mot de passe : <input type=\"password\" name=\"mdp_connec\" required></label><br/>")
	print ("<input type=\"button\" name=\"btn\" value=\"Connection\">")
	print ("</form>")



#def inscription():
#	#Pour récupérer les post du formulaire d'inscription : 
#	formData = cgi.FieldStorage()
#	nom_inscr = formData.getvalue('nom_inscr')
#	prenom_inscr = formData.getvalue('prenom_inscr')
#	genre_inscr = formData.getvalue('genre_inscr')
#	ddn_inscr = formData.getvalue('ddn_inscr')
#	mdp_inscr = formData.getvalue('mdp_inscr')
#	email_inscr = formData.getvalue('email_inscr')
#	print "Nom : " + nom_inscr + "<br/>Prénom : " + prenom_inscr + "<br/>Genre : " + genre_inscr
#	print "<br/>Date de naissance : " + ddn_inscr + "<br/> mot de passe (à crypter !) : " + mdp_inscr
#	print "<br/>Email : " + email_inscr + "<br/>"
#	print "<br/>Maintenant il faut réussir à tout mettre dans la BDD ..."


#ce que va faire le programme
get_url = cgi.FieldStorage()

if get_url.getvalue('inscrip') == 'true':
	inscription()

if get_url.getvalue('modif') == 'true':
	modif()

if get_url.getvalue('connec') == 'true':
	connec()


print """</body>
</html>"""