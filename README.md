# Analyse multimodale de données d'athlètes

Agrégation, nettoyage et modélisation de données de suivi d'athlètes combinant
un capteur porté Fitbit, des questionnaires quotidiens et des déclarations
alimentaires.

Trois participants suivis du 1er novembre 2019 au 31 mars 2020.

## Objectifs

- Construire une table exploitable au pas participant-jour à partir de sources hétérogènes
- Caractériser la qualité et la complétude des données
- Construire un indice de readiness comme proxy de la capacité à performer
- Modéliser le risque de blessure et l'indice de readiness

## Installation

Python 3.10 ou supérieur.

```bash
git clone https://github.com/Kawkaw54/athlete-monitoring.git
cd athlete-monitoring
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Données

Les données ne sont pas versionnées. Créer un dossier `data/` à la racine et y
placer les dossiers participants.

```
data/
├── p01/
│   ├── fitbit/          calories, distance, steps, heart_rate,
│   │                    resting_heart_rate, sleep, exercise,
│   │                    time_in_heart_rate_zones (JSON)
│   ├── pmsys/           wellness.csv, srpe.csv, injury.csv
│   ├── googledocs/      reporting.csv
│   └── food-images/     photographies des repas
├── p03/
├── p05/
└── participant-overview.xlsx
```

## Exécution

```bash
jupyter notebook analysis_athlete.ipynb
```

Exécuter les cellules dans l'ordre. Le notebook est structuré selon les quatre
blocs de l'énoncé :

1. Database handling — audit, agrégation, données nutritionnelles
2. Overview — structure, complétude, distributions
3. Pre-processing — types, valeurs aberrantes, valeurs manquantes
4. Modeling — variables construites, indice, deux modèles

Le temps de traitement est dominé par le chargement des flux de fréquence
cardiaque (1,5 million de mesures par participant) et par l'extraction des
métadonnées d'images.

Le script d'extraction EXIF peut être lancé indépendamment :

```bash
python src/metadonnees_images.py
```

## Livrables

| Fichier | Contenu |
|---|---|
| `test_dataset.csv` | table nettoyée, 456 lignes × 52 colonnes |
| `rapport_analyse_athletes.docx` | rapport de synthèse |
| `analysis_athlete.ipynb` | analyse complète et code |

Les valeurs manquantes sont conservées dans le jeu de données livré. Ce choix
est documenté en section 3 du notebook : aucune des cinq méthodes d'imputation
comparées n'apporte de gain mesurable, et l'autocorrélation à un jour est trop
faible pour justifier une propagation temporelle.
