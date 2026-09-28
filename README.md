# TriageBot

Outil en ligne de commande qui analyse les tickets de support du jeu Dungeon Delivery avec un modèle Ollama local.

## Prérequis

- Python 3.14
- Ollama installé et lancé
- Modèle `gemma3:4b` disponible

## Installation sous Windows

Dans le dossier du projet, ouvrir un terminal `cmd` :

```cmd
py -3.14 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
ollama pull gemma3:4b
```

Si le modèle est déjà installé, la dernière commande n'est pas nécessaire.

## Lancement

Vérifier que `tickets.json` se trouve dans le dossier du projet et qu'Ollama fonctionne, puis lancer :

```cmd
python main.py
```

Le programme crée `results.json` et `report.md`, et affiche un tableau de bord dans le terminal.

## Fonctionnement

Pour chaque ticket utilisable, TriageBot demande une analyse structurée au modèle et valide la réponse. Il réessaie au maximum deux fois si la réponse est invalide. Les messages vides ou repérés comme tentatives de manipulation sont signalés pour relecture. Les doublons d'un même joueur ne sont analysés qu'une fois.

Les règles d'escalade sont appliquées en Python : toxicité vers la modération, paiement d'urgence 4 ou 5 vers le responsable support, et tickets `to_check` vers une relecture humaine. Un brouillon de réponse est préparé pour les tickets analysés.

## Fichiers

- `tickets.json` : tickets à traiter
- `main.py` : programme
- `requirements.txt` : dépendances Python
- `results.json` : résultats détaillés après exécution
- `report.md` : synthèse destinée au support