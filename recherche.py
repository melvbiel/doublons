import os

# Catégorisation des extensions
EXTENSIONS = {
    "texte": {".txt", ".doc", ".docx", ".odt", ".csv", ".xls", ".ppt", ".odp"},
    "image": {".jpg", ".png", ".bmp", ".gif", ".svg"},
    "vidéo": {".mp4", ".avi", ".mov", ".mpeg", ".wmv"},
    "audio": {".mp3", ".mp2", ".wav", ".bwf"},
}

def somme_taille_fichiers(repertoire):
    """ Calcule la somme des tailles des fichiers par catégorie """
    tailles = {cat: 0 for cat in EXTENSIONS}  # Initialisation des catégories
    tailles["autre"] = 0  # Ajout d'une catégorie "autre"

    for racine, _, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            chemin_complet = os.path.join(racine, fichier)
            extension = os.path.splitext(fichier)[1].lower()
            taille = os.path.getsize(chemin_complet)

            # Trouver la catégorie du fichier
            for categorie, exts in EXTENSIONS.items():
                if extension in exts:
                    tailles[categorie] += taille
                    break
            else:
                tailles["autre"] += taille  # Si aucune catégorie ne correspond

    return tailles

# Exemple d'utilisation
repertoire_a_analyser = "C:\\Users\\melvy\\Desktop\\Algo"  # À remplacer par le chemin du dossier
resultat = somme_taille_fichiers(repertoire_a_analyser)

# Affichage des résultats
for categorie, taille in resultat.items():
    print(f"Total {categorie} : {taille} octets")
