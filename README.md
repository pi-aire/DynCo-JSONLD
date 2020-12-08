# DynCo-JSONLD
### BRUNEAU Richard - VASLIN Pierre

## Les fichiers principaux
Le fichier contenant le context : [context.json](https://github.com/pi-aire/DynCo-JSONLD/blob/main/src/context.json)

Le fichier n-quads : [result.nq](https://github.com/pi-aire/DynCo-JSONLD/blob/main/src/result.nq)

Le code Python : [toRDF.py](https://github.com/pi-aire/DynCo-JSONLD/blob/main/src/toRDF.py)

## Démarrage rapide

La commande permettant de produire le graphe RDF au format n-quads :
`cd ./src && python ./toRDF.py`

La commande permettant de vérifier SHACL sur votre machine : 
`cd ./src && pyshacl -s ../data/trace_model.shacl.ttl -f human result.nq`
