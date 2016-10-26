/*****************
** Author : Léa 
** Name : Formulaire.js
******************/

function changerimg() {
	alert("On doit importer une image ... Python ou js ? Hm ..");
}


function affichFormInscr() {
	if ($("#affichform").html()!="") {
		$("#affichform").html("");
	} else {
		$.get("Formulaire.py?inscrip=true",function(data,status) {
			$("#affichform").html($(data).filter("#inscription"));
			//$("#affichform").html($(data).find("inscription").html());
		});
	}
}

function affichFormModif() {
	if ($("#affichform").html()!="") {
		$("#affichform").html("");
	} else {
		$.get("Formulaire.py?modif=true",function(data,status) {
			$("#affichform").html($(data).filter("#modif"));
			//$("#affichform").html($(data).find("inscription").html());
		});
	}
}

function affichFormConec() {
	if ($("#affichform").html()!="") {
		$("#affichform").html("");
	} else {
		$.get("Formulaire.py?connec=true",function(data,status) {
			$("#affichform").html($(data).filter("#connec"));
			//$("#affichform").html($(data).find("inscription").html());
		});
	}
}


function js_inscription() {
	nom_inscr = nom_inscr.value;
	prenom_inscr = prenom_inscr.value;
	ddn_inscr = ddn_inscr.value;
	email_inscr = email_inscr.value;
	mdp_inscr = mdp_inscr.value;

	//Appeler Formulaire.py avec get ça sert à mettre les infos dans la BDD en fait
	$.get('Formulaire.py?inscrip=oui&nom_inscr='+nom_inscr+'&prenom_inscr='+prenom_inscr+'&genre_inscr='+genre_inscr+'&ddn_inscr='+ddn_inscr+"&email_inscr="+email_inscr+"&mdp_inscr="+mdp_inscr,function(data,status){
	});

}

//Formulaire.py?inscrip=oui&nom_inscr=essainom&prenom_inscr=essaiprenom&&genre_inscr=genreessai&ddn_inscr=13/10/1996&email_inscr=email@essai.fr&mdp_inscr=essaimdp


