/*****************
** Author : Léa 
** Name : Formulaire.js
******************/

/*Permet d'aller chercher une image dans l'ordinateur de l'utilisateur*/
function changerimg() {
	alert("On doit importer une image ... Python ou js ? Hm ..");
}


/*Affiche le formulaire d'inscription*/
function affichFormInscr() {
	alert("Bl");
	$.get("Formulaire.py?inscrip=true",function(data,status) {
		d = ($(data).filter("#inscription").html());
		if ($("#affichform").html()==d) {
			$("#affichform").html("");
		} else {
			$("#affichform").html(d);
			//$("#affichform").html($(data).find("inscription").html());
		}
	});
}

/*Affiche le formulaire de connection*/
function affichFormConec() {
	$.get("Formulaire.py?connec=true",function(data,status) {
		d = ($(data).filter("#connec").html());
		if ($("#affichform").html()==d) {
			$("#affichform").html("");
		} else {
			$("#affichform").html(d);
		}
	});
}
/*Affiche le formulaire de modification des infos, si l'utilisateur est déjà connecté*/
function affichFormModif() {
	$.get("Formulaire.py?modif=true",function(data,status) {
		d = ($(data).filter("#modif").html());
		if ($("#affichform").html()==d) {
			$("#affichform").html("");
		} else {
			$("#affichform").html(d);
		}
	});
}


function js_inscription() {
	nom_inscr = nom_inscr.value;
	prenom_inscr = prenom_inscr.value;
	ddn_inscr = ddn_inscr.value;
	email_inscr = email_inscr.value;
	mdp_inscr = mdp_inscr.value;
	//Appeler Formulaire.py avec get ça sert à mettre les infos dans la BDD en fait
	$.get('Formulaire.py?ajout_inscrip=true&nom_inscr='+nom_inscr+'&prenom_inscr='+prenom_inscr+'&genre_inscr='+genre_inscr+'&ddn_inscr='+ddn_inscr+"&email_inscr="+email_inscr+"&mdp_inscr="+mdp_inscr,function(data,status){
	});
}
//Formulaire.py?inscrip=oui&nom_inscr=essainom&prenom_inscr=essaiprenom&&genre_inscr=genreessai&ddn_inscr=13/10/1996&email_inscr=email@essai.fr&mdp_inscr=essaimdp

function js_connection() {
	email_connec = email_connec.value;
	mdp_connec = mdp_connec.value;
	$.get('Formulaire.py?connection=true&email_connec='+email_connec+"&mdp_connec"+mdp_connec,function(data,status){
	});
}
//Formulaire.py?connection=true&email_connec=essai@email.fr&mdp_connec=mdpessai

function js_modif() {
	//Comment faire pour récupérer la photo ?
	nom_modif = nom_modif.value;
	prenom_modif = prenom_modif.value;
	autrepren_modif = autrepren_modif.value;
	genre_modif = genre_modif.value;
	ddn_modif = ddn_modif.value;
	mdp_modif = mdp_modif.value;
	email_modif = email_modif.value;
	postal_modif = postal_modif.value;
	profession_modif = profession_modif.value;
	descr_modif = descr_modif.value;

	$.get('Formulaire.py?modif_fait=truenom_modif='+nom_modif+'&prenom_modif='+prenom_modif+'&autrepren_modif='+autrepren_modif+'&genre_modif='+genre_modif+'&ddn_modif='+ddn_modif+'mdp_modif='+mdp_modif+'&email_modif='+email_modif+'&postal_modif='+postal_modif+'&profession_modif='+profession_modif+'&descr_modif='+descr_modif,function(data,status){
	});
}

