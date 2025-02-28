import os
import hashlib
import time
from collections import defaultdict

#Exercice 1

def lister_fichiers_recursivement(repertoire):
    liste_fichiers = []
    for racine, _, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            liste_fichiers.append(os.path.join(racine, fichier))
    return liste_fichiers

def normaliser_nom(nom_fichier):
    suffixes = [' (1)', ' - copie', ' - copy']
    for suffix in suffixes:
        if nom_fichier.endswith(suffix):
            nom_fichier = nom_fichier[:-len(suffix)]
    return nom_fichier

def calculer_md5(file_path):
    with open(file_path, 'rb') as f:
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def comparer_fichiers(fichier1, fichier2):
    if fichier1['taille'] != fichier2['taille']:
        return False

    if fichier1['date_modification'] != fichier2['date_modification']:
        return False

    hash1 = calculer_md5(fichier1['chemin'])
    hash2 = calculer_md5(fichier2['chemin'])
    return hash1 == hash2

def trouver_fichiers_en_double(repertoire):
    fichiers_par_nom = defaultdict(list)
    
    fichiers = lister_fichiers_recursivement(repertoire)
    
    for fichier in fichiers:
        nom_normalise = normaliser_nom(os.path.basename(fichier))
        fichiers_par_nom[nom_normalise].append(fichier)
    

    doublons = []
    for nom, fichiers in fichiers_par_nom.items():
        if len(fichiers) > 1:

            fichiers_par_taille = defaultdict(list)
            for fichier in fichiers:
                taille = os.path.getsize(fichier)
                fichiers_par_taille[taille].append(fichier)
            

            for taille, fichiers_meme_taille in fichiers_par_taille.items():
                if len(fichiers_meme_taille) > 1:

                    fichiers_par_date = defaultdict(list)
                    for fichier in fichiers_meme_taille:
                        date_modification = os.path.getmtime(fichier)
                        fichiers_par_date[date_modification].append(fichier)
                    

                    for date, fichiers_meme_date in fichiers_par_date.items():
                        if len(fichiers_meme_date) > 1:

                            fichiers_par_hash = defaultdict(list)
                            for fichier in fichiers_meme_date:
                                hash_md5 = calculate_md5(fichier)
                                fichiers_par_hash[hash_md5].append(fichier)

                            for hash, fichiers_meme_hash in fichiers_par_hash.items():
                                if len(fichiers_meme_hash) > 1:
                                    doublons.append(fichiers_meme_hash)
    
    return doublons

#Exercice 2
EXTENSIONS = {
    "texte": {".txt", ".doc", ".docx", ".odt", ".csv", ".xls", ".ppt", ".odp"},
    "image": {".jpg", ".png", ".bmp", ".gif", ".svg"},
    "vidéo": {".mp4", ".avi", ".mov", ".mpeg", ".wmv"},
    "audio": {".mp3", ".mp2", ".wav", ".bwf"},
}

def somme_taille_fichiers(repertoire):
    """ Calcule la somme des tailles des fichiers par catégorie """
    tailles = {cat: 0 for cat in EXTENSIONS}  # Initialisation des catégories
    tailles["autre"] = 0  # Au cas où une autre extension est présente

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
                tailles["autre"] += taille  # Pour le reste

    return tailles

#Exercice 3

def trouver_doublons_repertoires(repertoire1, repertoire2):
    """Comparer les fichiers entre deux répertoires et trouver les doublons"""
    fichiers_repertoire1 = trouver_fichiers_en_double(repertoire1)
    fichiers_repertoire2 = trouver_fichiers_en_double(repertoire2)

    fichiers_par_nom_repertoire1 = {}
    for fichier in fichiers_repertoire1:
        nom_base = os.path.basename(fichier)
        nom_normalise = normaliser_nom(nom_base)
        taille = os.path.getsize(fichier)
        date_modification = os.path.getmtime(fichier)

        if nom_normalise not in fichiers_par_nom_repertoire1:
            fichiers_par_nom_repertoire1[nom_normalise] = []

        fichiers_par_nom_repertoire1[nom_normalise].append({
            'chemin': fichier,
            'taille': taille,
            'date_modification': date_modification
        })

    doublons = []

    for fichier in fichiers_repertoire2:
        nom_base = os.path.basename(fichier)
        nom_normalise = normaliser_nom(nom_base)
        taille = os.path.getsize(fichier)
        date_modification = os.path.getmtime(fichier)

        if nom_normalise in fichiers_par_nom_repertoire1:
            for fichier_repertoire1 in fichiers_par_nom_repertoire1[nom_normalise]:
                if comparer_fichiers(fichier_repertoire1, {
                    'chemin': fichier,
                    'taille': taille,
                    'date_modification': date_modification
                }):
                    doublons.append(fichier)
                    break

repertoire = 'C:\\Users\\melvy\\Desktop\\Algo'
doublons = trouver_fichiers_en_double(repertoire)
# Exemple d'utilisation Exercice 1

for groupe in doublons:
    print("Fichiers en double:")
    for fichier in groupe:
        print(f"  - {fichier}")

if doublons == []:
    print("Aucun doublon dans le répertoire choisi")

repertoire_a_analyser = "C:\\Users\\melvy\\Desktop\\Algo"  
resultat = somme_taille_fichiers(repertoire_a_analyser)

# Affichage des résultats
for categorie, taille in resultat.items():
    print(f"Total {categorie} : {taille} octets")