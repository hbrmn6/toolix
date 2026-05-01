import pandas as pd 
import numpy as np
from toolix.indice import *
# -remove_row=la ligne que on veut effacer
# et si on veut passer un fonction faut rajouter les "" 

def remove_row(matr, i):
    indices = traiter_indice(i, len(matr))
    return matr.drop(index=indices)


def remove_col(matr, i):
    indices = traiter_indice(i, matr.shape[1],matr.columns)
    cols_a_supprimer = matr.columns[indices]#on transforme le numero de position (1,2,3)  en vrai nom de colonnes  PAR EXEMPLE donc indices retourne des valeurs et par exemple on a 2 IL PART CHERCEHER LE NOM DE COLONNE(dans matr.columns )POSITION  3
    return matr.drop(columns=cols_a_supprimer)

#toolix --i data.csv -insert_row=2,3
def insert_row(matr, param):
    position, valeur_str = param.split(",")
    pos = int(position) -1

    if valeur_str == "num":
        nouv_ligne = list(range(1, matr.shape[1] + 1)) #  num : de 1 jusqu a 7+1 8
    else:
        v = valeur_str
        nouv_ligne = [v] * matr.shape[1]   #on multiplie par le nombre de colonne de la matrice  pour avoir toute une ligne de la valeur

    avant = matr.iloc[:pos]
    apres = matr.iloc[pos:]
    nouv_matr = pd.concat([avant,
                       pd.DataFrame([nouv_ligne], columns=matr.columns),
                       apres])
    return nouv_matr.reset_index(drop=True)# la synchroni

#toolix --i data.csv -insert_col=2,3
def insert_col(matr, param):
    pos_str, valeur_str = param.split(",")
    pos = int(pos_str) - 1
    if valeur_str == "num":
        nouv_col = list(range(1, len(matr) + 1))
    else:
        nouv_col = [valeur_str] * len(matr)

    nouv_matr = matr.copy().astype(object)

    nouv_matr.insert(loc=pos, column="temp", value=nouv_col)
    nouv_matr.columns = range(nouv_matr.shape[1])

    return nouv_matr.reset_index(drop=True)



def assurer_taille(matr, ligne, colonne):
    while ligne >= len(matr):
        matr = insert_row(matr, str(len(matr)+1)+ ",0")
    while colonne >= matr.shape[1]:
        matr = insert_col(matr, str(matr.shape[1]+1)+",0")
    return matr

#toolix --i data.csv -insert_element_at=1,1,7
def insert_element_at(matr, param):
    parts = param.split(",", 2)
    if len(parts) != 3:
            print("erreur : vous devez entrer 3 parametres !")
    i_, j_, valeur = parts
    i = int(i_)  - 1
    j = int(j_)  - 1

    matr = assurer_taille(matr, i, j).astype(object)
    value = valeur.strip()
    if (value.startswith('"') ) or (value.startswith("'")):
        v = value[1:-1] #  prend la chaine  sans les "  "
    else:
        try:
            v=int(valeur)
        except ValueError:
            v = valeur
    matr.iat[i, j] = v
    return matr

#toolix --i data.csv -remove_element_at=1,1
def remove_element_at(matr, param):
    i_, j_ = param.split(",", 1)
    i = int(i_)  - 1
    j = int(j_)  - 1

    if i < 0 or i >= len(matr) or j < 0 or j >= matr.shape[1]:
            print("Erreur : ligne  et colonne hors limites")
    matr.iat[i, j] = -1 # le -1 represente une valeur supprimee
    #matr.iat[i, j] = pd.NA 
    return matr

#on l'utilise pas 
def replace_element_at(matr, param):
    parts = param.split(",", 2)
    if len(parts) != 3:
            print("erreur : vous devez entrer 3 parametres !")
    i_, j_, valeur = parts
    i = int(i_)   - 1
    j = int(j_)  - 1
    if i < 0 or i >= len(matr):
            print("Erreur : ligne " + i_ + " hors limites")
            return matr
    if j < 0 or j >= matr.shape[1]:
            print("Erreur : colonne " + j_ + " hors limites")
            return matr

    if (valeur.startswith('"') ) or (valeur.startswith("'")):
        v = valeur[1:-1]
    else:
        try:
            v = int(valeur)
        except ValueError:
            v = valeur
    matr = matr.astype(object)
    matr.iat[i, j] = v
    return matr

#toolix --i data.csv -sort_col=6,asc
def sort_col(matr, param):
    try:
        colonne, ordre = param.split(",")
        col = int(colonne) - 1
    except:
        print("erreur : format attendu colonne, ordre (ex 2, asc)")
        return matr

    if col < 0 or col >= matr.shape[1]:
        print("erreur : colonne hors limites")
        return matr

    df = matr.copy()
    col_name = df.columns[col]
    ordre = ordre.strip()

    if ordre not in ("asc", "desc"):
        print("erreur : l'ordre doit etre asc ou desc")
        return matr

    df[col_name] = pd.to_numeric(df[col_name], errors="coerce") # erreur de to_numeric par defaut nan 
    return df.sort_values(by=col_name, ascending=(ordre == "asc")).reset_index(drop=True)

#toolix --i data.csv -sort_row=6,asc
def sort_row(matr, param):
    try:
        ligne, ordre =param.split(",")
        row=int(ligne)  - 1  
    except :
        print(" Erreur : format  attendu ligne , ordre (ex 2, desc )")
        return matr
    if row < 0 or row>=matr.shape[0]:
        print("Erreur : lignes hors limites")
        return matr
    df= matr
    valeurs = df.iloc[row].astype(str)
    if ordre=="asc":
        cols_sorted =valeurs.sort_values(ascending=True).index
    elif ordre=="desc":
        cols_sorted =valeurs.sort_values(ascending=False).index
    else:
        print("Erreur : ordre doit etre asc ou desc ")
        return matr
    return matr.loc[:, cols_sorted] ## Prend toutes les lignes du DataFrame et les colonnes dans l'ordre indique par sorted_cols

#sans parametre
def transpose(matr):
    array= np.transpose(matr)
    return pd.DataFrame(array)

#sans parametre
def reverse_row(matr):
    return matr.iloc[::-1].reset_index(drop=True) #les lignes inverses

#sans parametre
def reverse_col(matr):
    matr_rev = matr.iloc[:, ::-1]          # on touche pas aux lignes et  on  inverse l ordre des colonnes
    matr_rev.columns = range(matr_rev.shape[1])     # on renumerote les colonnes 0,1,2
    return matr_rev

#on cree une matrie de 0.0
#toolix --i data.csv -create=10,10
def create(param):
    ligne, colonne = param.split(",")
    return pd.DataFrame( np.zeros((int(ligne),int(colonne))) )

 # param : "7,<,14" ou  # param : 7,"<"",14
def filter_row(matr, param):
    parts = param.split(",")
    if len(parts) != 3:
        print("Erreur: le format attendu ligne , operateur , valeur ")
        return matr

    ligne   = parts[0]  
    op      = parts[1]
    valeur  = parts[2]

    try:
        row = int(ligne)  - 1
    except ValueError:
        print("erreur ! le format attendu ligne , operateur , valeur ")
        return matr

    if row < 0 or row >= matr.shape[0]:
        print("erreur : la ligne hors limite")
        return matr

    try:
        val = float(valeur)
    except ValueError:
        print("erreur : la valeur doit etre numerique")
        return matr
  
    df = matr.apply(pd.to_numeric, errors="coerce")

    # pour chaque colonne de cette ligne, on teste directement
    for j in range(matr.shape[1]):
        x = df.iat[row, j]

        if op == ">" and not (x > val):
            matr.iat[row, j] = 0
        elif op == "<" and not (x < val):
            matr.iat[row, j] = 0
        elif op == ">=" and not (x >= val):
            matr.iat[row, j] = 0
        elif op == "<=" and not (x <= val):
            matr.iat[row, j] = 0
        elif op == "==" and not (x == val):
            matr.iat[row, j] = 0
        elif op == "!=" and not (x != val):
            matr.iat[row, j] = 0
        elif op not in (">", "<", ">=", "<=", "==", "!="):
            print("erreur ! operateur invalide (>, <, >=, <=, ==, !=)")
            return matr

    return matr

def filter_col(matr , param):
    parts = param.split(",")
    if len(parts) != 3:
        print("erreur: format attendu ligne , operateur , valeur ")
        return matr

    colonne = parts[0]
    op      = parts[1]
    valeur  = parts[2]

    try:
        col = int(colonne)  - 1
    except ValueError:
        print("Erreur ! format attendu ligne , operateur , valeur ")
        return matr

    if col < 0 or col >= matr.shape[1]:
        print("Erreur : ligne hors limite")
        return matr
    try:
        val = float(valeur)
    except ValueError:
        print("Erreur : valeur doit etre numerique")
        return matr

    df = matr.apply(pd.to_numeric, errors="coerce")

    
    # pour chaque ligne de cette colonne, on teste directement
    for i in range(matr.shape[0]):
        x = df.iat[i, col]

        if op == ">" and not (x > val):
            matr.iat[i, col] = 0
        elif op == "<" and not (x < val):
            matr.iat[i, col] = 0
        elif op == ">=" and not (x >= val):
            matr.iat[i, col] = 0
        elif op == "<=" and not (x <= val):
            matr.iat[i, col] = 0
        elif op == "==" and not (x == val):
            matr.iat[i, col] = 0
        elif op == "!=" and not (x != val):
            matr.iat[i, col] = 0
        elif op not in (">", "<", ">=", "<=", "==", "!="):
            print("Erreur : operateur invalide (>, <, >=, <=, ==, !=)")
            return matr
    return matr

def find(matr, valeur):
    resultats = []
    valeurs = valeur.split(",")
    for v in valeurs:
        for i in range(matr.shape[0]):
            for j in range(matr.shape[1]):
                cellule = matr.iloc[i, j]
                # comparer en nombre si possible
                try :
                    if float(cellule) == float(v):
                        resultats.append((i, j))
                except:
                    # sinon comparer en texte
                    if str(cellule) == str(v):
                        resultats.append((i, j))
    return resultats
    
def replace(matr, param):

    parts = param.split(",", 1)
    if len(parts) != 2:
        print("format attendu : ancien,nouveau")
        return matr

    ancien, nv = parts

    # on travaille tout en string pour éviter les conflits de type
    matr_replace = matr.copy().astype(str)
    matr_replace = matr_replace.replace(ancien, nv, regex=False)

    print("tous les", ancien, "ont été remplacés par", nv)
    return matr_replace

def pourcentage(matr, param):
    try:
        pct = int(param.strip().rstrip('%'))

        if pct <= 0 or pct > 100:
            print("erreur : pourcentage entre 1 et 100")
            return matr

        total_lignes = matr.shape[0]
        nblignes = (total_lignes * pct) // 100

        if nblignes == 0:
            print("Erreur : pourcentage trop faible ",pct,"% pour ",total_lignes," lignes")
            return matr

        matr_shuffled = matr.sample(frac=1).reset_index(drop=True)
        return matr_shuffled.iloc[:nblignes].reset_index(drop=True)

    except  :
        print(" ERREUR format : 20 ou 20%")
        return matr

def addition(matr, param):
    if not (param.endswith('.csv') or param.endswith('.txt')):
        print("Erreur : fichier.csv ou fichier.txt")
        return matr

    try:
        matr2 = pd.read_csv(param, dtype=object, sep=None, engine="python")

        if matr.shape != matr2.shape:
            print("Erreur : dimensions incompatibles")
            return matr

        # Essayer d'additionner en nombres, sinon laisser tel quel
        df1 = matr.apply(pd.to_numeric, errors='coerce')
        df2 = matr2.apply(pd.to_numeric, errors='coerce')

        result = df1 + df2
        result = result.where(pd.notna(df1) & pd.notna(df2), matr)

        print("addition terminee :", result.shape)
        return result

    except Exception:
        print("Erreur lecture ou ajout")
        return matr
def concat_col(matr,fichier):
    try:
        if not (fichier.endswith('.csv')or fichier.endswith('.txt')):
            print("Erreur : format.csv ou fichier.txt")
            return matr
        matr2=pd.read_csv(fichier)

        if matr.shape[0] !=matr2.shape[0]:
            print("Erreur : lignes incompatibles Mat1: ",matr.shape[0],"lignes | Mat2 : ",matr2.shape[0],"lignes")
            return matr

        result=pd.concat([matr.reset_index(drop=True), matr2.reset_index(drop=True)], axis=1)
        print("Concat_col  : ", result.shape)
        return result.reset_index(drop=True)
    except  :
        print("Erreur concat_col", fichier)
        return matr


def concat_row(matrice1, fichier):
    # On lit le fichier de la même façon que dans charger_fichier
    df = pd.read_csv(fichier, sep=None, header=None, engine="python")
    df = df.iloc[1:].reset_index(drop=True)        # on ignore la ligne de header
    df.columns = range(df.shape[1])               # colonnes 0,1,2...

    # On impose à matrice1 d'avoir les mêmes noms de colonnes
    matrice1.columns = range(matrice1.shape[1])

    # Concaténation verticale + réindexation
    result = pd.concat([matrice1, df], ignore_index=True)
    return result
