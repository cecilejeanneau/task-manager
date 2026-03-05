# Task Manager

## Installation & usage

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
python3 -m http.server 5173
```

## Quelques commandes `curl`

### Créer une tâche
```bash
curl -s -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Écrire tests API","description":"Ajouter des assertions sur /tasks"}' | jq
```

### Lister les tâches
```bash
curl -s http://127.0.0.1:8000/tasks | jq
```

### Mettre à jour une tâche
```bash
curl -s -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"DONE"}' | jq
```

### Supprimer une tâche
```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/1
```

# Configuration de la clé API

Créez un fichier `.env` dans le dossier `backend/` avec le contenu suivant :
    API_KEY=devsecops-demo-secret-CHANGEME
Ne poussez jamais votre vraie clé dans le dépôt !

# Configuration de la base de données

Ajoutez dans votre `.env` :
    DATABASE_URL=CHANGEME

# Qualité du code frontend

Pour vérifier la qualité du code JavaScript et CSS dans le dossier `frontend/` :
- Installe ESLint et Stylelint (si besoin) :
      npm install -g eslint stylelint stylelint-config-standard

- Pour vérifier le JS :
      cd frontend
      eslint app.js

- Pour vérifier le CSS :
      stylelint styles.css

Adaptez les règles dans `.eslintrc.json` et `.stylelintrc.json` selon vos besoins.

# Couverture de tests backend

Pour générer un rapport de couverture :

    pytest --cov=app backend/tests

Le rapport s’affichera dans le terminal. Pour un rapport HTML :

    pytest --cov=app --cov-report=html backend/tests

Le dossier htmlcov/ contiendra le rapport détaillé.

# Dépendances de test backend

Pour exécuter les tests backend, installez aussi httpx :

    pip install -r backend/requirements.txt

Cela installera toutes les dépendances nécessaires (dont httpx pour les tests FastAPI).

# Tests backend

Pour exécuter tous les tests backend avec la couverture :

    pip install -r backend/requirements.txt
    pip install pytest-benchmark
    PYTHONPATH=backend pytest --cov=backend/app backend/tests

Cela garantit que toutes les dépendances de test sont installées et que les imports fonctionnent.

# DevSecOps CI/CD – Documentation rapide

## 1. Qualité et tests
- Lint et tests unitaires backend (pytest, flake8) et frontend (ESLint, Jest, Playwright) sont lancés à chaque push/pull request.

## 2. Conteneurisation
- Les images Docker backend et frontend sont construites automatiquement.

## 3. Sécurité
- Scan de vulnérabilités sur les images Docker et la recette docker-compose avec Trivy.

## 4. Publication
- Les images sont poussées sur GitHub Container Registry (ghcr.io).

## 5. Déploiement
- Un fichier docker-compose.yml permet de lancer l’ensemble localement ou en production.

## 6. CI/CD
- Tout est automatisé via GitHub Actions dans .github/workflows/ci.yml.

---

### Lancer le projet localement
```bash
docker-compose up --build
```

### Accéder aux applications
- Backend : http://localhost:8000
- Frontend : http://localhost:8080

### Personnaliser la registry
- Modifier les tags dans le workflow CI si besoin.

### Sécurité
- Les scans Trivy sont visibles dans les logs CI.

---

Pour toute question, voir le workflow ou les Dockerfile pour adapter à vos besoins.
