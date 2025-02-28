import os
import hashlib
import time

def lister_fichiers_recursivement(repertoire):
    fichiers = []
    for racine, _, fichiers_dans_dossier in os.walk(repertoire):
        for fichier in fichiers_dans_dossier:
            fichiers.append(os.path.join(racine, fichier))
    return fichiers

def normaliser_nom(nom_fichier):
    suffixes = [' (1)', ' - Copie', ' - Copy']
    for suffix in suffixes:
        if nom_fichier.endswith(suffix):
            nom_fichier = nom_fichier[:-len(suffix)]
    return nom_fichier

def calculer_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
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

def trouver_fichiers_en_double(rep1, rep2):

    fichiers_rep1 = lister_fichiers_recursivement(rep1)
    fichiers_rep2 = lister_fichiers_recursivement(rep2)


    fichiers_par_nom_rep1 = {}
    for fichier in fichiers_rep1:
        nom_base = os.path.basename(fichier)
        nom_normalise = normaliser_nom(nom_base)
        taille = os.path.getsize(fichier)
        date_modification = os.path.getmtime(fichier)

        if nom_normalise not in fichiers_par_nom_rep1:
            fichiers_par_nom_rep1[nom_normalise] = []

        fichiers_par_nom_rep1[nom_normalise].append({
            'chemin': fichier,
            'taille': taille,
            'date_modification': date_modification
        })

    fichiers_en_double = []


    for fichier in fichiers_rep2:
        nom_base = os.path.basename(fichier)
        nom_normalise = normaliser_nom(nom_base)
        taille = os.path.getsize(fichier)
        date_modification = os.path.getmtime(fichier)

        if nom_normalise in fichiers_par_nom_rep1:
            for fichier_rep1 in fichiers_par_nom_rep1[nom_normalise]:
                if comparer_fichiers(fichier_rep1, {
                    'chemin': fichier,
                    'taille': taille,
                    'date_modification': date_modification
                }):
                    fichiers_en_double.append(fichier)
                    break 

    return fichiers_en_double

if __name__ == "__main__":
    rep1 = r"C:\\Users\\Kanek\\OneDrive\\Bureau\\Mon dossier"
    rep2 = r"C:\\Users\\Kanek\\OneDrive\\Bureau\\Mon dossier 1"


    doubles = trouver_fichiers_en_double(rep1, rep2)
    
    if doubles:
        print("Fichiers en double trouvés dans rep2:")
        for fichier in doubles:
            print(fichier)
    else:
        print("Aucun fichier en double trouvé dans rep2.")
