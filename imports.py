import pandas as pd
import numpy as np

# toolix --i data.csv -put_at=2,4,"data.csv"
def put_at(matr , param):
    try:
        ligne, colonne, fichier = param.split(",", 2)
        ligne = int(ligne) - 1
        colonne = int(colonne) - 1
    except ValueError:
        print("Erreur : format attendu put_at=ligne,colonne,fichier")
        return matr

    if ligne < 0 or colonne < 0:
        print("Erreur : indices negatifs interdits")
        return matr

    fichier = fichier.strip().strip("'")

    try:
        fich = pd.read_csv(fichier, header=None, sep=None, engine="python")
    except FileNotFoundError:
        print("Erreur : fichier introuvable :", fichier)
        return matr
    except Exception:
        print("Erreur : probleme de la lecture du fichier")
        return matr

    r, c = fich.shape
    max_lignes = max(matr.shape[0], ligne + r)
    max_colonnes = max(matr.shape[1], colonne + c)

    if matr.shape[0] < max_lignes or matr.shape[1] < max_colonnes:
        new_matr = pd.DataFrame(np.zeros((max_lignes, max_colonnes), dtype=object))
        new_matr.iloc[:matr.shape[0], :matr.shape[1]] = matr.values
        matr = new_matr
    matr.iloc[ligne:ligne+r, colonne:colonne+c] = fich.values
    return matr


def input(param):
    # param = '"fich.txt",3,9'

    # Séparer les trois morceaux
    parts = param.split(",")
    fichier = parts[0].strip().strip('"')
    start = int(parts[1])
    end = int(parts[2])

    # Lire tout le fichier en brut
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    # Prendre juste les lignes qu'on veut
    extraites = []
    for i in range(start, end + 1):
        extraites.append(lignes[i].strip())

    # Transformer chaque ligne en liste (séparée par virgule)
    data = []
    for ligne in extraites:
        data.append(ligne.split(","))

    # Construire la DataFrame
    df = pd.DataFrame(data)

    return df.astype(object)