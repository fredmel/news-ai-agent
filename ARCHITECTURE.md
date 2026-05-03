# AI News Agent - Structure Modulaire

## Architecture

Le projet a été réorganisé en modules séparés pour une meilleure maintenabilité :

### Structure des dossiers

```
news-ai-agent/
├── src/                    # Package principal
│   ├── __init__.py        # Initialisation du package
│   ├── config.py          # Configuration & Variables
│   ├── tools.py           # Outils (Tavily, Dev.to)
│   ├── agents.py          # Agents IA (chercheur, synthétiseur, éditeur)
│   ├── tasks.py           # Tâches coordonnées
│   └── main.py            # Logique principale du Crew
├── main.py                # Point d'entrée principal
├── requirements.txt       # Dépendances
├── synthesis/             # Sorties des synthèses
└── ARCHITECTURE.md        # Cette documentation
```

### Modules

#### 1. **src/config.py** - Configuration & Variables
- Chargement des variables d'environnement (.env)
- Initialisation des clients API (Tavily)
- Constantes de configuration (répertoire, horaire)
- Clés API centralisées

#### 2. **src/tools.py** - Outils
- `search_ai_news()` : Recherche d'actualités IA via Tavily
- `publish_devto_draft()` : Publication de brouillons sur Dev.to

#### 3. **src/agents.py** - Agents IA
- `researcher` : Collecte les actualités des sources officielles
- `synthesizer` : Synthétise les informations collectées
- `publisher` : Publie les synthèses sur Dev.to

#### 4. **src/tasks.py** - Tâches
- `research_task` : Recherche les actualités
- `synthesize_task` : Synthétise les résultats
- `publish_draft_task` : Publie les brouillons

#### 5. **src/main.py** - Logique du Crew
- Crée et configure le Crew (équipe d'agents)
- Fonction `run_daily_news_agent()` : Exécute le workflow complet

#### 6. **main.py** - Point d'entrée
- Importe depuis le package `src`
- Gère la planification quotidienne
- Point d'entrée principal de l'application

## Flux d'exécution

```
main.py (racine)
  ↓
src.main.run_daily_news_agent()
  ↓
src.config (charge les variables)
  ↓
src.agents + src.tasks (définit agents & tâches)
  ↓
src.tools (fournit les outils)
  ↓
Crew.kickoff() (exécute le workflow)
  ↓
Résultats sauvegardés dans synthesis/
```

## Utilisation

```bash
# Installation des dépendances
pip install -r requirements.txt

# Exécution
python main.py
```

## Avantages de cette structure

✅ **Séparation claire des responsabilités** - Chaque module a une fonction unique  
✅ **Package Python propre** - Structure `src/` avec imports relatifs  
✅ **Maintenance simplifiée** - Modifications isolées par domaine  
✅ **Réutilisabilité** - Import des modules ailleurs si nécessaire  
✅ **Testabilité** - Tests unitaires par module  
✅ **Scalabilité** - Ajout facile de nouveaux agents/tâches  
✅ **Organisation professionnelle** - Structure standard Python

