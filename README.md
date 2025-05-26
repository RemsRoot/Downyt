# Youtube Downloader - Downyt

Downyt est un outil qui permet de télécharger des vidéos youtube sous deux format ".mp4" (format vidéo) et ".mp3" (format musique). Il propose un interface avec deux pages :
1 - Page pour entrer le lien
2- Page qui permet de choisir les différents paramètres du fichier à télécharger

## Prérequis 
1. Avoir python installer et pouvoir le lancer avec la commande shell "python"
2. Avoir pip installé

## fichier 

- download_youtube : répertoire de téléchargement des fichiers
- iconbitmap.ico & logo.png: images pour l'interface des musiques
- shell_youtube_downloader.bat : fichier shell script windows
- app-V1.X.py : fichier du code python de l'application  

# Package

- pytube : package de gestion du lien youtube 
- wget : package de gstion du téléchagement de la vidéo
- os : package de gestion des commandes du systeme
- tkinter : package de gestion de l'interface graphique
- pillow (PIL) : package de gestion des images
- math : pour la fonction ceil (arrondis entier supérieur)

# Lancement de l'app

lancer la commande :
./shell_youtube_downloader.bat

# VERSION

## Version 1.1

Création : 15/11/2023

Création de la première version de l'app

## Version 1.2

Mise à jour : 23/05/2025

Réglage de l'erreur "HTTP Error 400: Bad Request" 

1. Changement du package

installation du nouveau package : pytubefix
Remplacement de l'ancien package : pytube -> pytubefix

2. Réglage erreur du codec en vidéo/audio

3. Problème de doublon audio

## Version 2.1

Ajout des métadonnées automatiques

1. Gestion de l'erreur lors d'un second téléchagement d'un même fichier qui génère un fichier ".m4a"
