import eyed3
from eyed3.id3.frames import PictureFrame

def modifier_metadonnees(mp3_file, artiste, album, titre, jaquette_path=None):
    try:
        # Charger le fichier MP3
        audio_file = eyed3.load(mp3_file)

        # Vérifier si le fichier contient des métadonnées
        if audio_file.tag is None:
            print(f"Aucune métadonnée trouvée. Création d'une nouvelle étiquette pour {mp3_file}.")
            audio_file.tag = eyed3.id3.tag.Tag()

        # Modifier les métadonnées
        audio_file.tag.artist = artiste
        audio_file.tag.album = album
        audio_file.tag.title = titre
        audio_file.tag.track_num = 1  # Tu peux ajuster le numéro de la piste si nécessaire

        # Ajouter une jaquette si le chemin est fourni
        if jaquette_path:
            try:
                with open(jaquette_path, "rb") as img_file:
                    img_data = img_file.read()

                # Ajouter ou modifier la couverture
                audio_file.tag.frame_set["APIC"] = [
                    PictureFrame(
                        encoding=3,  # UTF-8
                        mime_type="image/jpeg",  # Type MIME de l'image
                        picture_type=3,  # Type de l'image (3 signifie une jaquette d'album)
                        description="Album art",  # Description de l'image
                        data=img_data  # Données de l'image
                    )
                ]
                print(f"Jaquette ajoutée avec succès depuis {jaquette_path}.")
            except Exception as e:
                print(f"Erreur lors de l'ajout de la jaquette : {e}")

        # Sauvegarder les modifications
        audio_file.tag.save()
        print("Les métadonnées ont été modifiées avec succès !")

    except Exception as e:
        print(f"Erreur lors de la modification du fichier {mp3_file}: {e}")
        
        # Exemple d'utilisation
modifier_metadonnees(
    "ton_fichier.mp3",  # Remplace par le chemin de ton fichier MP3
    artiste="Nom de l'artiste",
    album="Nom de l'album",
    titre="Titre de la chanson",
    jaquette_path="jaquette.jpg"  # Remplace par le chemin de ton image de jaquette
)