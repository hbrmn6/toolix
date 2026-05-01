import pandas as pd 
from toolix.indice import * 



def compute(df, fonction, axis):
    # On convertit en numérique et on remplace les non-convertibles par NaN
    df = df.apply(pd.to_numeric, errors="coerce")
    if fonction == "average":
        return df.mean(axis=axis)
    elif fonction == "sum":
        return df.sum(axis=axis)
    elif fonction == "min":
        return df.min(axis=axis)
    elif fonction == "max":
        return df.max(axis=axis)
    elif fonction in ("std", "stddev"):
        return df.std(axis=axis)
    elif fonction == "stats":
        somme = df.sum(axis=axis)
        moyenne = df.mean(axis=axis)
        std = df.std(axis=axis)
        return somme, moyenne, std
    else:
        print("Fonction inconnue :", fonction)
        return None

def compute_row(matr, param):
    fonction, inside = param.split("(", 1)
    inside = inside[:-1].strip()
    
    if inside == "all":
        list_ligne = list(range(matr.shape[0]))
    else:
        list_ligne = traiter_indice(inside, matr.shape[0])
   
    if not verifier_indices(list_ligne, matr.shape[0]):
        return matr

    lignes_ok = []

    for i in list_ligne:
        ligne = matr.iloc[i, :]

        est_numerique = True
        for val in ligne:
            try:
                float(val)
            except (ValueError, TypeError):
                est_numerique = False
                break

        if not est_numerique:
            print("La ligne " , i+1 , " contient une chaîne de caractères ou une valeur non numérique, elle est ignorée")
        else:
            lignes_ok.append(i)

    if not lignes_ok:
        print("Aucune ligne entièrement numérique, aucun calcul effectué")
        return matr

    # On ne sélectionne que les lignes OK
    matrice_select = matr.iloc[lignes_ok, :]

    result = compute(matrice_select, fonction, axis=1)
    if result is None:
        return matr

    if fonction == "stats":
        somme, moyenne, std = result
        for res in (somme, moyenne, std):
            new_col = [None] * matr.shape[0]
            for k, ligne_idx in enumerate(lignes_ok):
                new_col[ligne_idx] = res.iloc[k]
            colonne_name = matr.shape[1]
            matr[colonne_name] = new_col
        return matr

    new_col = [None] * matr.shape[0]
    for k, ligne_idx in enumerate(lignes_ok):
        new_col[ligne_idx] = result.iloc[k]
    colonne_name = matr.shape[1]
    matr[colonne_name] = new_col
    return matr
    
def compute_col(matr, param):
    fonction, indices = param.split("(", 1)
    indices = indices[:-1].strip()

    df = matr.replace(-1, pd.NA)
    
    if indices == "all":
        liste_col = list(range(df.shape[1])) 
    else:
        liste_col = traiter_indice(indices, df.shape[1])
    
    if not verifier_indices(liste_col, df.shape[1]):
        return matr

    colonnes_ok = []

    for col in liste_col:
        serie = df.iloc[:, col]

        est_numerique = True
        for val in serie:
            try:
                float(val)
            except (ValueError, TypeError):
                est_numerique = False
                break

        if not est_numerique:
            print("La colonne " , col+1 , " contient une chaîne de caractères ou une valeur non numérique, elle est ignorée")
        else:
            colonnes_ok.append(col)

    if not colonnes_ok:
        print("Aucune colonne entièrement numérique, aucun calcul effectué")
        return matr

    matrice_select = df.iloc[:, colonnes_ok]

    result = compute(matrice_select, fonction, axis=0)
    if result is None:
        return matr

    if fonction == "stats":
        somme, moyenne, std = result
        for res in (somme, moyenne, std):
            new_ligne = [pd.NA] * matr.shape[1]
            for k, col_idx in enumerate(colonnes_ok):
                new_ligne[col_idx] = res.iloc[k]
            nouv_index = matr.shape[0]
            new_line = pd.DataFrame([new_ligne],
                                    columns=matr.columns,
                                    index=[nouv_index])
            matr = pd.concat([matr, new_line])
        return matr

    new_ligne = [pd.NA] * matr.shape[1]
    for k, col_idx in enumerate(colonnes_ok):
        new_ligne[col_idx] = result.iloc[k]

    nouv_index = matr.shape[0]
    new_line = pd.DataFrame([new_ligne],
                            columns=matr.columns,
                            index=[nouv_index])
    matr = pd.concat([matr, new_line])
    return matr


def podium(matr):
    try:
        mat_triee=matr.sort_values(by=matr.columns[-1],ascending=False).reset_index(drop=True)
        top3=mat_triee.head(3)
        print("podium : ")
        print(top3)
        return top3
    except Exception as e :
        print("Erreur : ",e)
        return matr

