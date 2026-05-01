def traiter_indice(valeur, taille, colonnes=None):
    indices = []

    if valeur == "odd":
        for i in range(taille):
            if i % 2 == 1:
                indices.append(i)

    elif valeur == "even":
        for i in range(taille):
            if i % 2 == 0:
                indices.append(i)

    elif valeur.startswith("func("):
        expr = valeur[5:-1]
        n = 0
        while True:
            try:
                val = eval(expr, {"n": n})
                if val < 0 or val >= taille:
                    break
                indices.append(val - 1)
                n += 1
            except:
                break

    else:
        parts = valeur.split(",")

        for p in parts:
            p = p.strip()

            # CAS NOM DE COLONNE
            if colonnes is not None and p in colonnes:
                indices.append(list(colonnes).index(p))
                continue

            if "-" in p:
                a, b = p.split("-")
                a = int(a) - 1
                b = int(b) - 1
                for k in range(a, b + 1):
                    indices.append(k)
            else:
                indices.append(int(p) - 1)

    return sorted(set(indices))


def verifier_indices(liste, max_size):
    for indice in liste:
        if indice < 0 or indice >= max_size:
            print("Erreur : indice", indice + 1, "hors limites")
            return False
    return True
