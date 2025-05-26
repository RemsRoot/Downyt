from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
import wget
import os
from math import ceil
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

from metadata import modifier_metadonnees

################# Gestion fichier #################
path = "download_youtube"

if not os.path.exists(path) :
    os.mkdir(path)  

# Récupère le chemin du dossier "Téléchargements" de l'utilisateur courant
downloads_path = Path.home() / "Downloads"

# Nom du fichier jaquette
name_jaquette = path + '\\jaquette.jpg'

################# Fonction de gestion des doublons en paramètres youtube ###############
def check_duplicate_trivial(items):
    list_ok = []
    for index_tot in range(len(items)) :
        ok = 0
        for index_boucle in range(index_tot+1, len(items)) :
            if str(items[index_tot]) == str(items[index_boucle]) : 
              ok = 1
        if ok == 0 :  
            list_ok.append(items[index_tot])
    return list_ok

################# Fonction de vérification du fichier de téléchagement ##################
def gestion_download_youtube() :
    list_files = os.listdir(path)
    for files in list_files :
        if files == 'jaquette.jpg' :
            continue
        if files.endswith(".mp4") :
            continue
        if files.endswith(".mp3") :
            continue
        if files.endswith(".m4a") :
            try :
                new_name = files[:-4] + ".mp3"
                os.rename(path + "\\" + files, path + "\\" + new_name)
                print(files + " -> " + new_name)
            except Exception as e:
                print("\nErreur app.py :", e)
        else :
            os.remove(path + "\\" + files)
      
####################### Fonction de gestion des nom d'artiste et de titres ##########
def name_artiste_titre(artiste, titre) :
    # Suppression des caractères et chaine problématique ou récurante sur le l'artiste
    chaine_interdit_artiste = [" - Topic", "\\", "/", " TV"]
    for chaine in chaine_interdit_artiste :
        artiste = artiste.replace(chaine, "")
    # Suppression des caractères et chaine problématique ou récurante sur le titre
    chaine_interdit_titre = [" (clip officiel)", " (Clip Officiel)"," (Clip officiel)", " [clip officiel]", " [Clip Officiel]"," [Clip officiel]", str(artiste).upper(), str(artiste).lower(), "*", " - ", "\\"]
    for chaine in chaine_interdit_titre :
        titre = titre.replace(chaine, "")
    return artiste, titre

################# Fonction pour afficher une nouvelle fenêtre ################
def afficher_nouvelle_fenetre():
    #Création du lien entre un objet et le lien youtube
    url = main_entree.get()
    # si le lien est valide
    try:
        contenu = main_entree.get()  # Récupère le contenu de l'Entry widget
        main_label.config(text=contenu + " doesn't exist")
        yt = YouTube(url) # créer l'objet youtube
    # Si le lien est non valide
    except VideoUnavailable:
        main_label.config(text=f'[UNAVAIBLE ERROR] Video \"{url}\" is unavaialable') # cas ou le lien indisponible
    except RegexMatchError:
        main_label.config(text=f'[ANY MATCHES] Video \"{url}\" doesn\'t exist') # cas ou le lien n'existe pas
    else :               
        # affiche si le lien existe sur la page principale

        main_label.config(text= f"\"{url}\" exist")
        
        # Créé la nouvelle fenêtre fille
        sub_window = tk.Toplevel(main_window)  # Crée une nouvelle fenêtre
        sub_window.title("Youtube downloader")
        sub_window.geometry("670x900")
        sub_window.configure(bg="#333333", padx=10, pady=10)

        # INFORMATIONS VIDEO
        titre = yt.title
        # nom de la chaine
        auteur = yt.author
        # nom du fichier sauvegardé
        auteur, titre = name_artiste_titre(auteur, titre)
        path_movie = auteur + " - " + titre
        
        
        # Téléchargement de l'image
    
        if os.path.isfile(name_jaquette):
            os.remove(name_jaquette)
        file_name = wget.download(yt.thumbnail_url, out=name_jaquette) # télécharge la vignette       
        # Fichier MP4 avec son et audio séparés
        yt_video = yt.streams.filter(only_video=True, custom_filter_functions=[lambda video: (video.video_codec[0:3] == "avc")]) # trier par codec : avc
        nb_param_video = len(check_duplicate_trivial(yt_video.order_by("resolution")))
        param_video = check_duplicate_trivial(yt_video.order_by("resolution"))
        # Fichier Audio MP3
        yt_audio = yt.streams.filter(only_audio=True, custom_filter_functions=[lambda video: (video.audio_codec[0:4] == "opus")]) # trier par codec : opus
        nb_param_audio = len(check_duplicate_trivial(yt_audio.order_by("abr")))
        param_audio = check_duplicate_trivial(yt_audio.order_by("abr"))
        # définit le nombre de ligne de la grille
        if nb_param_video >= nb_param_audio :
            N = nb_param_video
        else :
            N = nb_param_audio
            
        # paramètre grille pour centrer les objets
        sub_window.grid_columnconfigure(0, weight=1)
        for row in [0, 1, 2, N+3, N+4] :
            sub_window.grid_rowconfigure(row, weight=1) 
        
        # Charge une image
        hauteur, largeur = Image.open(file_name).size
        while(hauteur > 500) :
            hauteur = ceil(hauteur/1.1)
            largeur = ceil(largeur/1.1)

        sub_image = Image.open(file_name).resize((hauteur, largeur), Image.Resampling.LANCZOS)
        sub_photo = ImageTk.PhotoImage(sub_image)
        # Crée un label pour afficher l'image de la vidéo
        sub_label_image = tk.Label(sub_window, image=sub_photo)
        sub_label_image.photo = sub_photo
        sub_label_image.grid(row=0, column=0, columnspan=2)  # Affiche l'image sur deux colonnes
        # label qui affiche le titre de la vidéo
        sub_label_name = tk.Label(sub_window, relief=tk.SOLID, text=path_movie, font=("Helvetica", 10), bg="#f05a2D", width=80, height=3)
        sub_label_name.grid(row=1, column=0, columnspan=2)  
        
        # variable contenant toutes les résolutions disponibles
        resolution = []
        dico_resolution_itag = {}
        for nb in range(nb_param_video):
            resolution.append(param_video[nb].resolution)
            dico_resolution_itag[param_video[nb].resolution] = param_video[nb].itag
        list_resolution = []
        for key in dico_resolution_itag.keys() :
            list_resolution.append(str(key))
        # variable contenant toutes les résolutions disponibles    
        abr = []
        dico_abr_itag = {}
        for nb in range(nb_param_audio):
            abr.append(param_audio[nb].abr)
            dico_abr_itag[param_audio[nb].abr] = param_audio[nb].itag
        list_abr = []
        for key in dico_abr_itag.keys() :
            list_abr.append(str(key))
            
        # Créé la grille de checkbox avec label
        # label vidéo
        sub_label_video = tk.Label(sub_window, relief=tk.RIDGE, text="VIDEO", font=("Helvetica", 10), bg="#595959", fg= "white", width=35, height=1)
        sub_label_video.grid(row=2, column=0) 
        # label audio
        sub_label_audio = tk.Label(sub_window, relief=tk.RIDGE, text="AUDIO", font=("Helvetica", 10), bg="#595959", fg= "white", width=35, height=1)
        sub_label_audio.grid(row=2, column=1) 
        # fonction quand tu appuyes sur les boutons
        global option_select
        option_select = 0
        def button_click(nb):
            global option_select
            global audio_or_video
            global quality
            option_select = 1
            if nb < nb_param_video :
                audio_or_video = "v"
                quality = list_resolution[nb]
                sub_label_param.config(text= list_resolution[nb])
            else :
                audio_or_video = "a"
                quality = list_abr[nb-nb_param_video]
                sub_label_param.config(text= list_abr[nb-nb_param_video])
        # Affiche les boutons
        for row in range(3, nb_param_video+3):
            # Crée un checkbox
            bouton = tk.Checkbutton(sub_window, text=list_resolution[row-3], command=lambda row=row: button_click(row - 3), relief=tk.RIDGE, bg="#595959", fg= "white", highlightthickness= 0, font= ("Arial", 10, "bold"), width=35, height=2)
            bouton.grid(row=row, column=0)
        for row in range(3, nb_param_audio+3):
            # Crée un checkbox
            bouton = tk.Checkbutton(sub_window, text=list_abr[row-3], command=lambda row=row: button_click(row + nb_param_video - 3), relief=tk.RIDGE, bg="#595959", fg= "white", highlightthickness= 0, font= ("Arial", 10, "bold"), width=35, height=2)
            bouton.grid(row=row, column=1)
        
        # label qui affiche l'option
        sub_label_param = tk.Label(sub_window, relief=tk.SOLID, text="Selectionner un paramètre", font=("Helvetica", 10), bg="#f05a2D", width=80, height=3)
        sub_label_param.grid(row=N+3, column=0, columnspan=2)   
        # Bouton pour télécharger la vidéo
        def telecharger_video():
            # si une option a été sélectionnée
            if option_select == 1 :
                # retrouve itag lié à la qualité
                if audio_or_video == "a" :
                    itag = dico_abr_itag[quality]
                elif audio_or_video == "v" :
                    itag = dico_resolution_itag[quality]
                stream = yt.streams.get_by_itag(itag)
                # télécharge la vidéo
                if audio_or_video == "v" :
                    sub_label_param.config(text="EN COURS ...")
                    stream.download(output_path= path)

                else :
                    sub_label_param.config(text="EN COURS ...")
                    out_file = stream.download(output_path= path)
                    # sauvegarde au format mp3
                    
                    base, ext = os.path.splitext(out_file)
                    # ajout de "-file" au nom du fichier pour eviter un futur problème avec ffmeg qui réécrit sur le fichier en cas de nom identique 
                    new_file = base + '-file.mp3'
                    if not os.path.exists(new_file) :
                        os.rename(out_file, new_file)
                    else :
                        os.remove(new_file)
                # affiche la fin du téléchargement avec la taille du fichier
                if stream.filesize/1024 < 1000 :
                    sub_label_param.config(text= f"Download Finish - {stream.filesize/(1024):.2f} Ko")
                elif stream.filesize/(1024*1024) < 1000 :
                    sub_label_param.config(text= f"Download Finish - {stream.filesize/(1024*1024):.2f} Mo")
                else :
                    sub_label_param.config(text= f"Download Finish - {stream.filesize/(1024*1024):.2f} Go")
                gestion_download_youtube()
                # Si c'est une musique, il faut changer les métadonnées
                if audio_or_video != "v" :
                    file_name_final = str(downloads_path) + "\\" + auteur + " - " + titre.replace("/", "") + ".mp3"
                    modifier_metadonnees(new_file, file_name_final, titre, auteur, file_name)
                    if os.path.exists(new_file) :
                        os.remove(new_file)
            else :
                sub_label_param.config(text="NO OPTION SELECT")
            if audio_or_video == "v" :
                print("\n", "Auteur : ", auteur, "\n", "Titre  : ", titre, "\n")
            else : 
                print("\n", "Auteur : ", auteur, "\n", "Titre  : ", titre, "\n")   
        sub_bouton_telecharger = tk.Button(sub_window, text="Télécharger la vidéo", command=telecharger_video, width=70, height=3)
        sub_bouton_telecharger.grid(row=N+4, column=0, columnspan=2) # Affiche le bouton sur deux colonnes
        sub_bouton_telecharger.config(relief=tk.RAISED, bg="#595959", fg= "white", highlightthickness= 0, font= ("Arial", 15, "bold"))       
        
if __name__ == "__main__" :
    ################ Crée la fenêtre principale ################
    main_window = tk.Tk()
    main_window.title("Youtube downloader")
    main_window.geometry("700x400")
    main_window.configure(bg="#333333", padx=10, pady=10)

    ################# Ligne pour entrer du texte ################
    main_entree = tk.Entry(main_window, width=200, relief=tk.RIDGE)
    main_entree.pack(pady=10)

    ################# Bouton pour afficher une nouvelle fenêtre ################
    main_button = tk.Button(main_window, text="Générer les options de la vidéo", command=afficher_nouvelle_fenetre, bg="blue", fg="white", font=("Helvetica", 12))
    # Personnalise l'apparence du bouton
    main_button.config(relief=tk.RAISED, bg="#595959", fg= "white", highlightthickness= 0, font= ("Arial", 15, "bold"))  # Ajoute un effet de relief au bouton
    main_button.pack(pady=30)

    ################# Label de vérification ################
    main_label = tk.Label(main_window, relief=tk.SOLID, text="Vérifiation du lien", font=("Helvetica", 10), bg="#f05a2D", width=200, height=3)
    main_label.pack()

    # Nombre de lignes dans la grille (modifiez cette valeur selon vos besoins)
    labels = []  # Pour stocker les labels afin de les mettre à jour
            
    ################# Lancement de la boucle principale de l'interface graphique ################
    main_window.mainloop()