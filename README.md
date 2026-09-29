# Volatility Surface QA — Démonstration

Interface Python développée avec **Streamlit** pour comparer des surfaces de volatilité implicite entre deux dates et repérer les écarts dépassant un seuil de tolérance.

> **Ce dépôt est une version de démonstration d’un projet réalisé dans le cadre de mon stage. Le projet réel contient des données confidentielles et ne peut donc pas être partagé dans son intégralité. Cette démo présente le principe de l’interface et ses principales fonctionnalités à partir d’un jeu de données d’exemple.**

## Objectif

Faciliter le contrôle qualité des données de volatilité : sélectionner un instrument et deux dates, comparer les valeurs pour chaque couple strike/échéance commun, puis examiner les écarts dans un tableau et des graphiques par échéance.

## Fonctionnalités

- Import de données au format JSON.
- Choix de l’instrument, des deux dates de comparaison et du seuil de tolérance.
- Calcul des écarts absolus de volatilité entre les deux dates.
- Comptage et mise en évidence des lignes dépassant le seuil.
- Comparaison graphique des courbes de volatilité en fonction du strike, pour une échéance sélectionnée.
- Export Excel avec trois onglets : données de la première date, données de la seconde date et résultats de la comparaison.

## Technologies

Python, Streamlit, pandas, Matplotlib et openpyxl.

## Installation et lancement

Depuis le dossier du projet, installer les dépendances dans votre environnement Python :

```bash
python -m pip install streamlit pandas matplotlib openpyxl
```

Lancer l’interface :

```bash
python -m streamlit run user-interface.py
```

Ouvrir ensuite l’adresse locale affichée dans le terminal.

## Essayer la démo

1. Importer le fichier [`sample_data_august_2026.json`](sample_data_august_2026.json) depuis la barre latérale.
2. Conserver le nom d’instrument `demo_asset_v1`.
3. Sélectionner deux dates disponibles dans le fichier, la première précédant la seconde.
4. Renseigner le seuil de tolérance et cliquer sur **Run**.
5. Consulter les alertes, le tableau et les courbes par échéance, puis télécharger le rapport Excel si nécessaire.

La sélection des dates est actuellement limitée à **août 2026** dans cette démo.

## Format des données

Le fichier JSON doit contenir une liste d’observations, directement ou sous une clé `data`. Chaque observation comporte les champs suivants :

| Champ | Description |
| --- | --- |
| `instrument` | Nom de l’instrument |
| `trade_date` | Date d’observation au format `YYYY-MM-DD` |
| `strike` | Prix d’exercice |
| `expiry` | Date d’échéance au format `YYYY-MM-DD` |
| `vol` | Volatilité implicite numérique |

Exemple d’observation :

```json
[
  {
    "instrument": "demo_asset_v1",
    "trade_date": "2026-08-01",
    "strike": 100.0,
    "expiry": "2026-09-18",
    "vol": 20.5
  }
]
```

Une comparaison nécessite des observations sur deux dates, avec des couples strike/échéance communs. L’écart calculé est `abs(vol_date1 - vol_date2)` : le seuil s’exprime dans la même unité que les valeurs de volatilité. Pour une volatilité saisie comme `20.5` pour 20,5 %, un seuil de `0.01` correspond à 0,01 point de pourcentage.

## Structure du dépôt

```text
vol-surface-qa/
├── user-interface.py             # Interface Streamlit
├── fonction.py                   # Chargement, comparaison, graphiques et export
├── sample_data_august_2026.json   # Jeu de données d’exemple
└── README.md
```

Cette version sert à illustrer le travail réalisé et le parcours utilisateur ; elle ne représente pas l’ensemble du projet de stage.
