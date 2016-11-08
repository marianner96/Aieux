
DROP TABLE Utilisateur;
DROP TABLE Arbre;
DROP TABLE Famille;

-- id : identifiant unique de la famille
-- nom : nom de la famille
-- nombre_personnes : nombres de personnes présentes dans la famille
CREATE TABLE Famille (
	id INT CONSTRAINT pk_famille PRIMARY KEY,
	nom VARCHAR2(30) ,
	nombre_personnes SMALLINT
); 

-- id : identifiant unique de l'utilisateur
-- nom : nom de l'utilisateur
-- prenom : prénom de l'utilisateur
-- genre : genre de l'utilisateur
-- date_naissance : date de naissance de l'utilisateur
-- mdp : mot de passe chiffré
-- mail : e-mail de l'utilisateur
-- id_famille : identifiant de la famille si il y appartient
-- rang : droit de l'utilisateur
CREATE TABLE Utilisateur (
	id INT CONSTRAINT pk_utilisateur PRIMARY KEY,
	nom VARCHAR2(30),
	prenom VARCHAR2(30),
	genre CHAR(1),
	date_naissance DATE ,
	mdp VARCHAR2(30) ,
	mail VARCHAR2(30) ,
	id_famille REFERENCES famille(id) ,
	rang SMALLINT DEFAULT 0
);

-- id : identifiant unique de l'arbre de la famille
-- id_famille : identifiant de la famille auquel appartient l'arbre 
CREATE TABLE Arbre (
	id INT CONSTRAINT pk_arbre PRIMARY KEY,
	id_famille REFERENCES famille(id)
);