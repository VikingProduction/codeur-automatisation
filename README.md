# Automatisation de Soumission d'Offres sur Codeur

Ce projet a pour but d'automatiser la soumission d'offres sur la plateforme [Codeur](https://www.codeur.com/). Le script récupère le flux RSS des projets, filtre les offres récentes (publiées aujourd'hui et datant de moins de 30 minutes), vérifie qu'une offre n'a pas déjà été soumise (via le GUID), et publie une offre en se connectant automatiquement au site avec Selenium.

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Dépendances](#dépendances)
- [Avertissements et Remarques](#avertissements-et-remarques)
- [Licence](#licence)

## Fonctionnalités

- **Récupération du flux RSS :**  
  Le script se connecte à l'URL `https://www.codeur.com/projects?format=rss` pour récupérer les projets en cours.

- **Filtrage des offres :**  
  - Seules les offres publiées aujourd'hui et datant de moins de 30 minutes sont traitées.
  - Exclusion des projets dont le GUID a déjà été enregistré dans un log pour éviter les doublons.
  - Possibilité d'exclure certains projets en fonction de mots-clés dans le titre ou la description.

- **Détermination de l'offre :**  
  Le montant et la durée de l'offre sont calculés selon le budget indiqué dans la description du projet.

- **Messages tournants personnalisés :**  
  Des messages pré-enregistrés sont utilisés pour personnaliser la soumission de l'offre en remplaçant la variable `$title` par le titre du projet.

- **Automatisation via Selenium :**  
  Le script se connecte à Codeur via la page de connexion (https://www.codeur.com/users/sign_in) en remplissant automatiquement les champs `user_email` et `user_password`, puis soumet l'offre sur le projet concerné.

## Structure du Projet
project/
├── main.py                  # Script principal
├── exceptions.py            # Définitions des exceptions personnalisées
├── messages.py              # Gestion des messages tournants
├── posted_offers.txt        # Log des GUID des offres déjà soumises (créé automatiquement)
├── requirements.txt         # Liste des dépendances du projet
└── messages/                # Dossier contenant les fichiers de messages tournants
    ├── message1.txt
    └── message2.txt         # (optionnel)



## Installation

1. **Cloner le dépôt :**
   git clone https://votre-repo-url.git
   cd project

2.Installer les dépendances :
    Assurez-vous d'avoir Python 3.x installé, puis exécutez :
    pip install -r requirements.txt

  3. Installer le driver Selenium :
     Pour Google Chrome, téléchargez Chromedriver et placez-le dans votre PATH ou dans le répertoire du projet.

Utilisation
    Préparation des messages tournants :
        Modifiez ou ajoutez des fichiers dans le dossier messages/ avec vos modèles de messages. Utilisez la variable $title dans vos fichiers pour être remplacée par le titre du projet.
    Exécution du script :
      Lancez le script principal :
        python main.py
      Authentification sur Codeur :
          Lors de l'exécution, le script vous demandera d'entrer votre email et votre mot de passe pour vous connecter sur Codeur via la page Sign In.
      Suivi des offres soumises :
          Le script enregistre automatiquement le GUID de chaque offre soumise dans le fichier posted_offers.txt afin d'éviter de republier sur un même projet lors d'exécutions ultérieures.

## Configuration

    Mots-clés d'exclusion :
      Vous pouvez personnaliser la liste des mots-clés dans le fichier main.py (variable mots_exclusion) pour ignorer certains projets.
    Paramètres de l'offre :
      La fonction determiner_offre dans main.py définit le montant et la durée de l'offre en fonction du budget indiqué dans la description. Adaptez cette fonction en fonction de vos besoins.
    Vérification de la date :
      La fonction is_recent vérifie que le projet a été publié aujourd'hui et dans les 30 minutes précédentes. Vous pouvez modifier ce paramètre en ajustant le paramètre max_minutes.

## Dépendances

Les dépendances principales du projet sont :
    feedparser : Pour parser le flux RSS.
    selenium : Pour automatiser la navigation et la soumission d'offres via un navigateur.

Consultez le fichier requirements.txt pour plus de détails.

## Avertissements et Remarques

    Driver Selenium :
      Assurez-vous d'utiliser la version du driver correspondant à votre version du navigateur (par exemple, Chromedriver pour Google Chrome).
    Sécurité des identifiants :
      Les identifiants de connexion sont demandés via l'invite de commande. Pour une utilisation en production, envisagez de stocker ces informations dans des variables d'environnement ou un gestionnaire de secrets.
    Tests et robustesse :
      Bien que le script inclue des vérifications (dates, GUID, mots-clés d'exclusion), il est recommandé de le tester sur un environnement de test avant de l'utiliser en production.
    Évolution de l'interface :
      En cas de modification de l'interface ou de l'API de Codeur, certaines parties du script (notamment l'identification des éléments via Selenium) devront être mises à jour.

##  Licence

Ce projet est distribué sous Licence MIT avec interdiction formelle de vente.
Ce projet a été développé par https://viking-production.fr

Avertissements et Responsabilités
    Attention :
        Ce script est fourni à titre expérimental et ne garantit pas le respect des Conditions Générales d'Utilisation (CGU) de la plateforme Codeur.
    Utilisation sous votre responsabilité :
        L'utilisation de ce script peut violer les règles de la plateforme Codeur, ce qui pourrait entraîner la suspension ou le bannissement de votre compte.
        Les auteurs de ce projet ne sauraient être tenus responsables de tout dommage, suspension ou bannissement résultant de son utilisation.
    Conseils :
        Assurez-vous de bien lire et comprendre les CGU de Codeur avant d'utiliser ce script.
        Testez le script dans un environnement contrôlé et soyez conscient des risques encourus.

