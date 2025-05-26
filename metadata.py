import ffmpeg
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from mutagen.mp3 import MP3

# réalise la commande à appliquer avant : ffmpeg -i fichier_original.mp3 fichier_converti.mp3
def command_ffmeg(fichier_original, fichier_converti):
    music_file = ffmpeg.input(fichier_original)
    music_file.output(fichier_converti, loglevel="quiet").run()
    
# Charger les métadonnées du fichier MP3
def modifier_metadonnees(fichier_entree, fichier_sortie, titre, artiste, album) : 
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
    audio_file["TALB"] = TALB(encoding=3, text=album)  # Album

    # Sauvegarder les changements
    audio_file.save()
    print("Métadonnées mises à jour avec succès !")
    
if __name__ == "__main__" :
    fichier_entree = "VALD - TAL  TAL (clip officiel).mp3"
    fichier_sortie = "fichier_sortie.mp3"
    modifier_metadonnees(fichier_entree, fichier_sortie, "titre", "artiste", "album")