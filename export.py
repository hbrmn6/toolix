import pandas as pd 
import numpy as np 




#toolix --i data.csv -get_at=2,4,6,4
def get_at(matr, param):
    # param = "ligne,colonne,nb_lignes,nb_colonnes"
    try:
        ligne, colonne, nb_lignes, nb_colonnes = param.split(",", 3)
        ligne = int(ligne) - 1
        colonne = int(colonne)  - 1
        nb_lignes = int(nb_lignes) 
        nb_colonnes = int(nb_colonnes) 
    except:
        print("erreur : format attendu get_at=ligne,colonne,nb_lignes,nb_colonnes")
        return matr

    if ligne < 0 or colonne < 0:
        print("Erreur : indices negatifs interdits")
        return matr

    if ligne + nb_lignes > matr.shape[0] or colonne + nb_colonnes > matr.shape[1]:
        print("erreur : la zone demandee depasse la matrice")
        return matr

    bloc = matr.iloc[ligne:ligne+nb_lignes, colonne:colonne+nb_colonnes]
    return bloc


def output(matr, filename, prefix, suffix, separator):
    _,extension=filename.split(".")
    ext=extension.lower()
    if prefix is None:
        prefix = ""
    if suffix is None:
        suffix = ""
    if separator is None:
        separator = ","
    if ext == "csv":
        separator=";"

        matr.to_csv(filename, index=False, header=False , sep=separator)

    elif ext == "html":
        matr.to_html(filename, index=False, header=False)

    elif ext in ("cpp", "h"):
        prefix="{"
        suffix="}"
        separator=","
        with open(filename, "w", encoding="utf-8") as f:
            f.write("// Matrice générée par toolix\n")
            f.write("const int N_ROWS = %d;\n" % matr.shape[0])
            f.write("const int N_COLS = %d;\n\n" % matr.shape[1])
            f.write("int matrix[N_ROWS][N_COLS] = {\n")
            for i, row in enumerate(matr.values):
                valeurs = separator.join(str(v) for v in row)
                sep = "," if i < matr.shape[0] - 1 else ""
                ligne = "    " + prefix + valeurs + suffix + sep + "\n"
                f.write(ligne)
            f.write("};\n")

    elif ext == "json":
        matr.to_json(filename, orient="values")
    
    elif ext == "tex":
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\\begin{tabular}{" + "c" * matr.shape[1] + "}\n")
            for _, row in matr.iterrows():
                ligne = " & ".join(str(v) for v in row.values)
                f.write(ligne + " \\\\\n")
            f.write("\\end{tabular}\n")
    else:
        with open(filename, "w", encoding="utf-8") as f:
             for row in matr.values:
                valeurs = separator.join(str(v) for v in row)
                ligne = prefix + valeurs + suffix + "\n"
                f.write(ligne)

    print("Exporté :" ,filename)
