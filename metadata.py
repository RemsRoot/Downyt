import ffmpeg
from mutagen.id3 import ID3, TIT2, TPE1, APIC
from mutagen.mp3 import MP3

# réalise la commande à appliquer avant : ffmpeg -i fichier_original.mp3 fichier_converti.mp3
def command_ffmeg(fichier_original, fichier_converti):
    music_file = ffmpeg.input(fichier_original)
    music_file.output(fichier_converti, loglevel="quiet", y=None).run() # le rend silencieux et accepte automatiquement la réécriture
    
# Charger les métadonnées du fichier MP3
def modifier_metadonnees(fichier_entree, fichier_sortie, titre, artiste, file_jacquette) : 
    try:
        # Création d'un nouveau fichier avec la possibilité d'ajout de métadonnées
        command_ffmeg(fichier_entree, fichier_sortie)
        # charge les métadonnées
        audio_file = MP3(fichier_sortie, ID3=ID3)
    # Cas d'erreur   
    except Exception as e:
        print("Erreur metadata.py :", e)
        
    # ouvre le fichier et lit les métadonnées
    audio_file.tags = ID3()
    # Modifier les tags
    audio_file["TIT2"] = TIT2(encoding=3, text=titre)  # Titre
    audio_file["TPE1"] = TPE1(encoding=3, text=artiste)  # Artiste
    
    # image jacquette
    try :
        with open(file_jacquette, 'rb') as img:
            audio_file.tags.add(
                APIC(
                    encoding=3,         # 3 = UTF-8
                    mime='image/jpeg',  # ou 'image/png' selon ton image
                    type=3,             # 3 = image de couverture (front cover)
                    desc='Cover',
                    data=img.read()
                )
            )
    except :
        print("Pas de fichier de couverture")
        
    # Sauvegarder les changements
    audio_file.save()
    print("\nMétadonnées mises à jour avec succès !")
    
if __name__ == "__main__" :
    prinf("OK")
