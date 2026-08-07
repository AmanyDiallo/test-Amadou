# Guide de déploiement AWS — pile serverless (FastAPI + Lambda + DynamoDB) et frontend Amplify

Ce document décrit, pas-à‑pas, la création du compte AWS, la préparation locale, le déploiement du backend avec AWS SAM et le déploiement du frontend sur AWS Amplify.

## 1. Prérequis
- Compte AWS (email + carte bancaire)
- Machine Linux/WSL/macOS avec `curl`, `unzip`, `git`, `python3` et `docker` (pour tests SAM locaux)

## 2. Création du compte AWS et sécurité
1. Allez sur https://aws.amazon.com/ et créez un nouveau compte.
2. Activez MFA sur le compte root : Console → votre nom → `Security Credentials` → `Multi-Factor Authentication`.
3. Créez un utilisateur IAM (ex: `deploy-admin`) :
   - Console → IAM → `Users` → `Add user`.
   - Cochez `Programmatic access` et `AWS Management Console access`.
   - Créez un groupe `Administrators` et attachez la policy `AdministratorAccess`.
   - Téléchargez la paire `Access Key ID` / `Secret Access Key` (conservez-les dans un gestionnaire de mots de passe).
4. Activez MFA sur l'utilisateur IAM (profil utilisateur → `Security credentials` → `Manage MFA`).
5. Créez un budget (Billing → Budgets) avec une alerte par e‑mail (ex : 5 USD) pour éviter les surprises.

## 3. Préparer l'environnement local
### Installer AWS CLI v2
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Installer Docker (pour SAM local)
```bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
```

### Installer Python venv et SAM CLI
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install aws-sam-cli
```

### Configurer l'interface en ligne de commande AWS
Après avoir créé l'utilisateur IAM `deploy-admin`, exécutez :
```bash
aws configure
# Entrez Access Key ID, Secret Access Key, région par défaut (ex: eu-west-3), output json
```

## 4. Déployer le backend (AWS SAM)
Fichiers importants dans le repo:
- `infra/template.yaml` — template SAM (Lambda + DynamoDB + API)
- `backend/` — code FastAPI + handler Mangum

Commandes (depuis la racine du repo) :
```bash
cd /workspaces/test-Amadou
sam build --template-file infra/template.yaml
sam deploy --guided --template-file infra/template.yaml --stack-name test-amadou-stack
```
Lors du `--guided`, acceptez la création de rôles IAM si demandé et notez les outputs (notamment `ApiUrl`).

Après déploiement, récupérez l'URL API (depuis la sortie du `sam deploy` ou CloudFormation Outputs).

## 5. Mettre à jour le frontend avec l'API URL
Remplacez `<API_URL_PLACEHOLDER>` dans `frontend/index.html` par l'URL retournée (`ApiUrl`). Vous pouvez le faire manuellement ou via le script `scripts/update_frontend_api_url.sh` fourni.

## 6. Déployer le frontend sur Amplify
1. Poussez le repo sur GitHub (branche `main`).
2. Console AWS → Amplify → `Get started` → Connect app → sélectionnez GitHub et autorisez.
3. Sélectionnez le repo `test-Amadou` et la branche `main`.
4. Root directory: `frontend/` (aucune build si simple `index.html`).
5. Dans `Environment variables`, ajoutez `API_URL` si vous préférez ne pas modifier `index.html` directement.
6. Déployez. Amplify fournira une URL publique du type `https://branch.appid.amplifyapp.com`.

## 7. Bonnes pratiques et nettoyage
- Supprimez les ressources de test quand vous n'en avez plus besoin (`aws cloudformation delete-stack --stack-name test-amadou-stack`).
- Activez CloudWatch et budgets d'alerte (Billing alarms).
- Ne partagez jamais vos clés AWS.

## 8. Scripts fournis
- `scripts/deploy_backend.sh` : lance `sam build` puis `sam deploy --guided`.
- `scripts/update_frontend_api_url.sh` : remplace `<API_URL_PLACEHOLDER>` dans `frontend/index.html` par l'URL fournie.

---
Si vous voulez, je peux :
- Exécuter un commit avec ces fichiers et pousser sur le repo distant (nécessite que vous me donniez la télécommande ou que vous le fassiez localement).
- Générer des captures d'écran pas-à-pas pour la création du compte AWS.
