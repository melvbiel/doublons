import os
import hashlib
import shutil

def lister_fichiers_recursivement(repertoire):
    fichiers = []
    for racine, _, fichiers_dans_repertoire in os.walk(repertoire):
        for fichier in fichiers_dans_repertoire:
            fichiers.append(os.path.join(racine, fichier))
    return fichiers

def calculate_md5(file_path):
    with open(file_path, 'rb') as f:
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

def obtenir_date_modification(file_path):
    return os.path.getmtime(file_path)

def synchroniser_repertoires(rep1, rep2):
    fichiers_rep1 = lister_fichiers_recursivement(rep1)
    fichiers_rep2 = lister_fichiers_recursivement(rep2)

    fichiers_rep1_dict = {os.path.basename(f).lower(): f for f in fichiers_rep1}
    fichiers_rep2_dict = {os.path.basename(f).lower(): f for f in fichiers_rep2}

    print(f"Fichiers dans {rep1} : {fichiers_rep1}")
    print(f"Fichiers dans {rep2} : {fichiers_rep2}")


    for fichier_rep2 in fichiers_rep2:
        nom_fichier = os.path.basename(fichier_rep2).lower()
        chemin_fichier_rep1 = os.path.join(rep1, os.path.basename(fichier_rep2))

        if nom_fichier in fichiers_rep1_dict:
            date_modif_rep1 = obtenir_date_modification(fichiers_rep1_dict[nom_fichier])
            date_modif_rep2 = obtenir_date_modification(fichier_rep2)

            if date_modif_rep2 > date_modif_rep1:
                shutil.copy2(fichier_rep2, chemin_fichier_rep1)
                print(f"Fichier {nom_fichier} mis à jour dans {rep1}")
        else:
            shutil.copy2(fichier_rep2, chemin_fichier_rep1)
            print(f"Fichier {nom_fichier} copié dans {rep1}")

    for fichier_rep1 in fichiers_rep1:
        nom_fichier = os.path.basename(fichier_rep1).lower()
        chemin_fichier_rep2 = os.path.join(rep2, os.path.basename(fichier_rep1))

        if nom_fichier in fichiers_rep2_dict:
            date_modif_rep1 = obtenir_date_modification(fichier_rep1)
            date_modif_rep2 = obtenir_date_modification(fichiers_rep2_dict[nom_fichier])

            if date_modif_rep1 > date_modif_rep2:
                shutil.copy2(fichier_rep1, chemin_fichier_rep2)
                print(f"Fichier {nom_fichier} mis à jour dans {rep2}")
        else:
            shutil.copy2(fichier_rep1, chemin_fichier_rep2)
            print(f"Fichier {nom_fichier} copié dans {rep2}")

rep1 = os.path.abspath(r"C:\Users\Kanek\OneDrive\Bureau\Mon dossier")
rep2 = os.path.abspath(r"C:\Users\Kanek\OneDrive\Bureau\Mon dossier 1")

synchroniser_repertoires(rep1, rep2)
