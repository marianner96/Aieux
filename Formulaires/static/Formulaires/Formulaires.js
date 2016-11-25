//Pour Form_event.py, lorsqu'on clique sur un événement, affiche le div d'en dessous
//avec le formulaire associé à l'événement. 
function affiche(mot) {
	if (document.getElementById(mot).style.display == "block") {
		document.getElementById(mot).style.display = "none";
	} else {
		document.getElementById(mot).style.display = "block";
	}
}

//Pour Form_modif.py et aussi le profil normalement, permet d'afficher l'image
function affich_img() {
	alert("blbl");
	alert(document.getElementById('img').src);
	document.getElementById('img').src = "profil_chat.jpg";
}