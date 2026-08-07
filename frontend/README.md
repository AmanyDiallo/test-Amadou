# Frontend minimal

Ce frontend est une page HTML statique minimale. Pour déployer sur AWS Amplify :

1. Pousser ce dépôt sur GitHub
2. Dans la console AWS Amplify, créer une nouvelle app et connecter le repo
3. Utiliser le dossier `frontend/` comme racine de build (aucun build nécessaire pour index.html)
4. Après le déploiement, remplacer `<API_URL_PLACEHOLDER>` par l'URL fournie par le template SAM (ou config via variables d'environnement Amplify)
