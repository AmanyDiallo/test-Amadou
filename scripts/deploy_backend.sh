#!/usr/bin/env bash
set -euo pipefail

# Script pour builder et déployer la stack SAM
# Usage: ./scripts/deploy_backend.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Building SAM application..."
sam build --template-file infra/template.yaml

echo "Launching sam deploy --guided (interactive)..."
sam deploy --guided --template-file infra/template.yaml --stack-name test-amadou-stack

echo "Déploiement terminé. Récupérez ApiUrl depuis la sortie ou CloudFormation Outputs."
