"""Extrait les dates de prise de vue des photographies de repas."""

import pandas as pd
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

BASE = Path("data")
PARTICIPANTS = ["p01", "p03", "p05"]


def lire_date_image(chemin):
    """Retourne la date de prise de vue depuis les metadonnees EXIF."""
    try:
        exif = Image.open(chemin)._getexif()
        if not exif:
            return None
        for tag_id, valeur in exif.items():
            if TAGS.get(tag_id) == "DateTimeOriginal":
                return pd.to_datetime(valeur, format="%Y:%m:%d %H:%M:%S")
    except Exception:
        return None
    return None


def extraire_dossier(dossier, participant):
    """Parcourt un dossier d'images et retourne un tableau des prises de vue."""
    lignes = []
    for f in Path(dossier).iterdir():
        if not f.is_file() or f.name.startswith("."):
            continue
        d = lire_date_image(f)
        lignes.append({"participant": participant, "fichier": f.name,
                       "horodatage": d, "exif_present": d is not None})
    return pd.DataFrame(lignes)


if __name__ == "__main__":
    tout = pd.concat([
        extraire_dossier(BASE / p / "food-images", p)
        for p in PARTICIPANTS
        if (BASE / p / "food-images").exists()
    ])
    tout.to_csv("metadonnees_images.csv", index=False)
    print(f"{len(tout)} images, {tout['exif_present'].sum()} avec EXIF exploitable")