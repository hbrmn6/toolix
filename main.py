
import argparse
import sys
import os
import pandas as pd
from toolix.operation import *
from toolix.indice import *
from toolix.calculs import *
from toolix.export import *
from toolix.imports import *

def decouper_en_blocs(argv):
    blocs = []
    blocs_restore = []

    action_encours = None          # bloc normal en cours
    bloc_restore_encours = None    # bloc restore en cours

    i = 0

    while i < len(argv):
        arg = argv[i]

        if arg.startswith("--restore="):
            # si un bloc normal est  en cours  on le termine
            if action_encours:
                blocs.append(action_encours)
                action_encours = None

            # nouveau bloc pr restorer
            index = int(arg.split("=", 1)[1])
            bloc_restore_encours = {"restore": index, "cmds": []}
            blocs_restore.append(bloc_restore_encours)

            i += 1
            continue

        # si on est dans un bloc restore 
        if bloc_restore_encours is not None:
            if arg in ("-i", "--input"):
                bloc_restore_encours = None
                continue  

            cmd = arg.lstrip("-")
            if "=" in cmd:
                name, param = cmd.split("=", 1)
            else:
                name, param = cmd, None
            blocs_restore[-1]["cmds"].append((name, param))

            i += 1
            continue

        if arg == "-i":
            if action_encours:
                blocs.append(action_encours)

            i += 1
            fichier = argv[i]
            action_encours = {"file": fichier, "header": "", "cmds": []}

            i += 1
            continue

        if arg.startswith("--input="):
            # si aucun bloc n'existe on crée un bloc vide
            if action_encours is None:
                action_encours = {"file": None, "header": "", "cmds": []}

            # ajouter la commande input dans le bloc
            name = "input"
            param = arg.split("=", 1)[1]
            action_encours["cmds"].append((name, param))

            i += 1
            continue

        # Header
        elif arg.startswith("--header="):
            action_encours["header"] = arg.split("=", 1)[1]

        # Create
        elif arg.startswith("--create="):
            if action_encours:
                blocs.append(action_encours)
            param = arg.split("=", 1)[1]
            action_encours = {"file": None, "header": "", "cmds": [("create", param)]}

        # Commande 
        else:
            cmd = arg.lstrip("-")
            if "=" in cmd:
                name, param = cmd.split("=", 1)
            else:
                name, param = cmd, None
            action_encours["cmds"].append((name, param))

        i += 1

    if action_encours:
        blocs.append(action_encours)

    return blocs, blocs_restore


def appliquer_commande(matrice, name, param, options):
    if name == "input":
        return input(param)
    elif name == "remove_row":
        return remove_row(matrice, param)
    elif name == "remove_col":
        return remove_col(matrice, param)
    elif name == "insert_row":
        return insert_row(matrice, param)
    elif name == "insert_col":
        return insert_col(matrice, param)
    elif name == "insert_element_at":
        return insert_element_at(matrice, param)
    elif name == "remove_element_at":
        return remove_element_at(matrice, param)
    elif name == "replace_element_at":
        return replace_element_at(matrice, param)
    elif name == "compute_col":
        return compute_col(matrice, param)
    elif name == "compute_row":
        return compute_row(matrice, param)
    elif name == "sort_row":
        return sort_row(matrice, param)
    elif name == "sort_col":
        return sort_col(matrice, param)
    elif name == "transpose":
        return transpose(matrice)
    elif name == "reverse_row":
        return reverse_row(matrice)
    elif name == "concat_row":
        return concat_row(matrice,param)
    elif name == "concat_col":
        return concat_col(matrice,param)
    elif name == "reverse_col":
        return reverse_col(matrice)
    elif name == "create":
        return create(param)
    elif name == "put_at":
        return put_at(matrice, param)
    elif name == "filter_row":
        return filter_row(matrice, param)
    elif name == "filter_col":
        return filter_col(matrice, param)
    elif name == "replace":
        return replace(matrice, param)
    elif name == "get_at":
        return get_at(matrice, param)
    elif name == "pourcentage":
        return pourcentage(matrice, param)
    #elif name == "addition":
      #  return addition(matrice, param)
    elif name == "find":
        print(find(matrice, param))
        return matrice
    elif name == "podium":
        podium(matrice)
        return matrice
    elif name == "output":
        output(matrice, param, options.prefix, options.suffix, options.separator)
        return matrice
    else:
        print("Commande inconnue :", name)
        return matrice



def charger_fichier(fichier, header):
    df = pd.read_csv(fichier, sep=None, header=None,engine="python")

    if header == "no":
        df = pd.read_csv(fichier, header=None,skiprows=1, sep=None, engine="python")
        df.columns = range(df.shape[1])
    elif header =="yes" :
        df = pd.read_csv(fichier, header=0, sep=None, engine="python")

    return df.astype(object)


def main():
    _help_path = os.path.join(os.path.dirname(__file__), "help.txt")
    with open(_help_path, "r", encoding="utf-8") as f:
        epilog_text = f.read()

    parser = argparse.ArgumentParser(
        description="Toolix — Outil de manipulation de matrices",
        formatter_class=argparse.RawTextHelpFormatter,
        usage="toolix -i fichier -commandes",
        epilog=epilog_text
    )

    parser.add_argument("--prefix", default=" ")
    parser.add_argument("--suffix", default=" ")
    parser.add_argument("--separator", default=" ")

    options, commandes = parser.parse_known_args()

    #decoupage en blocs normaux + blocs restore
    blocs, blocs_restore = decouper_en_blocs(commandes)

    matr_enregistres = []

    for bloc_index, bloc in enumerate(blocs, start=1):
        fichier = bloc["file"]
        header = bloc["header"]
        cmds = bloc["cmds"]

        if fichier:
            matrice = charger_fichier(fichier, header)
        else:
            matrice = pd.DataFrame()

        if not matrice.empty:        # Afficher la matrice initiale seulement si elle n'est pas vide
            print("\n bloc ",bloc_index," : matrice initiale ")
            print(matrice)

        for name, param in cmds:
            matrice = appliquer_commande(matrice, name, param, options)

        print("\n bloc ",bloc_index,": matrice finale  ")
        print(matrice)

        matr_enregistres.append(matrice.copy())

   
    for bloc_r in blocs_restore:
        index = bloc_r["restore"] - 1

        if 0 <= index < len(matr_enregistres):
            matrice = matr_enregistres[index].copy()
            print("\n matrice restaurée (bloc ",index+1,") ")
            print(matrice)
        else:
            print("Erreur : index restore invalide")
            continue

        for name, param in bloc_r["cmds"]:
            matrice = appliquer_commande(matrice, name, param, options)

        print("\nmatrice finale RESTORE")
        print(matrice)


if __name__ == "__main__":
    main()

