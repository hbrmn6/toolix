# toolix
Toolix est un outil en ligne de commande permettant de manipuler des matrices directement depuis le terminal Linux : chargement intelligent, transformations, statistiques, concaténation, filtrage, tri, import/export multi‑formats. 

## Installation
'''bash
pip install -e .
## Utilisation
toolix -i data.csv [options]
## Commandes principales

Structure
--create=n,m
--header=yes|no|par defaut(tt en data)
# Insertion
--insert_row=INDEX,VALUE
--insert_col=INDEX,VALUE
--insert_element_at=i,j,val
--put_at=i,j,fichier.csv
--concat_row=fichier
--concat_col=fichier
# Suppression
--remove_row=INDICES
--remove_col=INDICES
--remove_element_at=i,j
# Calculs
--compute_row=func(indices)
--compute_col=func(indices)

# Fonctions :
     sum | average | min | max | std | stats

# Transformations
--transpose
--reverse_row
--reverse_col
--sort_row=indices,asc|desc
--sort_col=indices,asc|desc
# Filtrage / recherche
--filter_row=ROW,op,val
--filter_col=COL,op,val
--find=VAL
--replace=VAL1,VAL2
--pourcentage=PCT
# Export
--output=fichier.ext

Formats : csv , json , html , latex , cpp

# Options :

--prefix=PREFIX
--suffix=SUFFIX
--separator=SEP
# Autres
--input="file",start,end
--restore=N
--podium
--get_at=i,j,n,m
# Indices
odd / even
1-5 (range)
1,3,7 (list)
func(n*2)
# Exemples
toolix -i data.csv --header=yes
toolix --create=10,20 --transpose
toolix --create=10,20 --compute_col="average(all)"
toolix --create=10,20 --remove_row=2-5
toolix -i data.csv --sort_row=3,asc
toolix --input="data.csv",2,8 --compute_col="sum(all)"
