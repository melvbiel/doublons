import os
import hashlib
import time
from collections import defaultdict

def lister_fichiers_recursivement(repertoire):
    fichiers = []
    for racine, _, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            fichiers.append(os.path.join(racine, fichier))
    return fichiers

def normaliser_nom(nom_fichier):
    suffixes = [' (1)', ' - copie', ' - copy']
    for suffix in suffixes:
        if nom_fichier.endswith(suffix):
            nom_fichier = nom_fichier[:-len(suffix)]
    return nom_fichier

def calculate_md5(file_path):
    with open(file_path, 'rb') as f:
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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

repertoire = 'C:\\Users\\Kanek\\OneDrive\\Bureau\\Mon dossier'
doublons = trouver_fichiers_en_double(repertoire)

for groupe in doublons:
    print("Fichiers en double:")
    for fichier in groupe:
        print(f"  - {fichier}")