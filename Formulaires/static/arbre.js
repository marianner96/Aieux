var DIR = '/static/img/';

var nodes = null;
var edges = null;
var network = null;
var layoutMethod = "directed";

//Charge puis dessine l'arbre généalogique
function charge_arbre() {
    maj_nodes_edges();
    //Lis le fichier nodesedges.json via javascript
    $.getJSON("/static/json/nodesedges.json",function( data ) {

            /*console.log("données JSON lues: ");
            console.log(data); */
            console.log("Exemples: ");
            console.log(data.nodes[1]); 
            console.log(data.edges[1]);

            var nodes = [];
            var edges = [];

            //Les noeuds
            for(var i= 0; i < data.nodes.length; i++)
            {
                nodes.push(data.nodes[i]);
            }

            //Les liens
            for(var j= 0; j < data.edges.length; j++)
            {
                edges.push(data.edges[j]);
            }

            console.log("Mes nodes: ");
            for(var k=0; k<nodes.length; k++){
                console.log(nodes[k]);
            }

            console.log("Mes liens: ");
            for(var m=0; m<edges.length; m++){
                console.log(nodes[m]);
            }

            //alert("Dessin des noeuds et des liens... ");
            draw(nodes, edges);
    });
}


//Va chercher dans le fichier nodesedges.json la liste des noeuds et la met à jour au besoin (cad si le fichier modifs n'est pas vide)
function maj_nodes_edges(){
    $.ajax({
        url:'/maj_nodes_edges/',
        type:'get',
    });
}

//Dessine l'arbre généalogique (le réseau) à partir de la liste des noeuds et des liens passé en paramètre
function draw(nodes, edges) {
    destroy();
    var container = document.getElementById('mynetwork');

    var data = { //Les données
        nodes: nodes,
        edges: edges
    };

    var options = { //Les options
        layout: {
            hierarchical: {
                sortMethod: "directed"
            }
        },
        edges: {
            smooth: true,
            arrows: {to : true }
        },
        interaction: {
            hover:true
        }
    };

    // Cree un reseau
    network = new vis.Network(container, data, options);

    network.on("click", function (params) {
        params.event = "[original event]";
        var parametres = JSON.stringify(params);

        console.log(parametres);

        var elementClique = "";
        var indice = 10;

        while (parametres[indice]!=']'){
            elementClique=elementClique+parametres[indice];
            indice++;
        }

        document.getElementById('eventSpan').innerHTML = "L'élément sélectionné est le: "+elementClique;

        if (elementClique==14){
            document.location.href="/hello"; 
        }
    });
}

//Réinitialise le réseau
function destroy() {
  if (network !== null) {
        network.destroy();
        network = null;
  }
}


//Au changement du radio (enfant, parent ou conjoint) change le contenu du formulaire
function deroule_suite(radio){
    var valeur_radio = radio.value;
    var enf = document.getElementById("form_enfant");
    var par = document.getElementById("form_parent");
    var conj = document.getElementById("form_conjoint");
    var choix_radio = document.getElementById("choix_radio");

    switch(valeur_radio) {
        case "enfant":
            enf.style.display="inline";
            par.style.display="none";
            conj.style.display="none";
            choix_radio.value="enfant";
            break;
        case "parent":
            enf.style.display="none";
            par.style.display="inline";
            conj.style.display="none";
            choix_radio.value="parent";
            break;
        case "conjoint":
            enf.style.display="none";
            par.style.display="none";
            conj.style.display="inline";
            choix_radio.value="conjoint";
            break;
    }
}


//Au sumbit de l'ajout d'un nouveau membre enregistre les données dans la BDD
function maj_nouv_membre(){
    var type_membre = document.getElementById("choix_radio").value;
    var nom = document.getElementById("nom_membre_add").value;
    var prenom = document.getElementById("prenom_membre_add").value;
    var sexe = document.getElementById("feminin").checked;
    if (sexe){sexe="f";} else{sexe="m"}

    switch(type_membre) {
        case "enfant":
            var parents = document.getElementById("liste_couples").value; //qui sont les parents de l'enfant à rajouter
            //Met à jour la liste des personnes sans conjoint
            maj_liste_sans_conj(nom,prenom,sexe);
            //Met à jour le fichier modifs.json
            modifs('enfant',parents,nom,prenom,sexe);
            break;

        case "parent":
            var enfant = document.getElementById("liste_enfants_sans_parents").value ; //à quel enfant est lié le parent à rajouter
            //Met à jours les listes concernant le nouveau membre
            maj_listes_nouv_parent(enfant,nom,prenom,sexe);
            //Met à jour le fichier modifs.json
            modifs('parent',enfant,nom,prenom,sexe);
            break;

        case "conjoint":
            var conj = document.getElementById("liste_personnes_sans_conjoint").value ; //à quel enfant est lié le parent à rajouter
            //Met à jour les listes concernant le nouveau membre
            maj_listes_nouv_couple(conj,nom,prenom,sexe);
            //Met à jour le fichier modifs.json
            modifs('couple',conj,nom,prenom,sexe);
            break;
    } 
}

//Actualise les listes suivantes: couples, enfants et personne sans conjoint
function maj_listes_nouv_parent(enfant,nom,prenom,sexe){
    $.ajax({
        url:'/maj_lnp/',
        type:'get',
        data:{
            sonenfant:enfant,
            sonnom:nom,
            sonprenom:prenom,
            sonsexe:sexe
        }
    });
}

//Actualise la liste des personnes sans conjoints dans le fichier liste_sans_conj.json
function maj_liste_sans_conj(nom,prenom,sexe,conjoint) {
    $.ajax({
        url:'/maj_lsc/',
        type:'get',
        data:{
            sonnom:nom,
            sonprenom:prenom,
            sonsexe:sexe
        }
    });
}


//Met à jour les listes suivantes: couples, enfants, personne sans conjoint
function maj_listes_nouv_couple(conjoint,nom,prenom,sexe){
    $.ajax({
        url:'/maj_lnc/',
        type:'get',
        data:{
            sonconjoint:conjoint,
            sonnom:nom,
            sonprenom:prenom,
            sonsexe:sexe
        }
    });
}

//Met à jour le fichier modifs.json
function modifs(typep,lien,nom,prenom,sexe){ //on ajoute un membre, le lien correspond à papa et maman si on ajoute un enfant par exemple
    alert("Maj fichier modifs!");

    $.ajax({
        url:'/modifierfichier/',
        type:'get',
        data:{
            sontype:typep,
            sonlien:lien,
            sonnom:nom,
            sonprenom:prenom,
            sonsexe:sexe
        }
    });
}



//Met à jour les options des selects pour qu'ils proposent les nouveaux membres ajoutés
function maj_options(){
    alert("maj options!");
    var liste_c = document.getElementById("liste_couples");
    var liste_e = document.getElementById("liste_enfants_sans_parents");
    var liste_sc = document.getElementById("liste_personnes_sans_conjoint");

    //Ajout de toutes les options pour la liste des couples, cad ajout des couples au select
    $.getJSON("/static/json/liste_couples.json",function( data ) {
        tab = data.couples;
        alert("Maj option liste couples")
        console.log("Taille du tableau contenant les couples: ")
        console.log(tab.length);

        for (var i=0; i<(tab.length); i++){
            var option_c = document.createElement("option");
            infos = tab[i];
            couple = infos["nom"]+" "+infos["prenom"]+" - "+infos["nom2"]+" "+infos["prenom2"];
            option_c.text = couple;
            liste_c.add(option_c);
        }
    });


    $.getJSON("/static/json/liste_enfants.json",function( data ) {
        tab = data.orphelins;
        alert("Maj options listes enfants");
        console.log("Taille du tableau contenant les orphelins: ");
        console.log(tab.length);

        for (var i=0; i<(tab.length); i++){
            var option_e = document.createElement("option");
            infos = tab[i];
            enfant = infos["nom"]+" "+infos["prenom"];
            option_e.text = enfant;
            liste_e.add(option_e);
        }
    });

    $.getJSON("/static/json/liste_sans_conj.json",function( data ) {
        tab = data.sansconj;
        alert("Maj options des sans conjoints")
        //console.log(tab.length);

        for (var i=0; i<(tab.length); i++){
            var option_sc = document.createElement("option");
            infos = tab[i];
            celibataire = infos["nom"]+" "+infos["prenom"];
            option_sc.text = celibataire;
            liste_sc.add(option_sc);
        }
    });
}










