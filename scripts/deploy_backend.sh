#!/usr/bin/env bash
set -euo pipefail

# Script pour builder et déployer la stack SAM
# Usage: ./scripts/deploy_backend.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SAM_BIN="$ROOT_DIR/.venv/bin/sam"
cd "$ROOT_DIR"

if [ ! -x "$SAM_BIN" ]; then
  echo "Erreur : sam CLI introuvable dans $SAM_BIN" >&2
  echo "Assure-toi d'avoir installé aws-sam-cli dans .venv et de l'activer." >&2
  exit 1
fi

echo "Building SAM application..."
"$SAM_BIN" build --template-file infra/template.yaml

BUILD_TEMPLATE="$ROOT_DIR/.aws-sam/build/template.yaml"
if [ ! -f "$BUILD_TEMPLATE" ]; then
  echo "Erreur : template build introuvable dans $BUILD_TEMPLATE" >&2
  exit 1
fi

echo "Launching sam deploy --guided (interactive)..."
"$SAM_BIN" deploy --guided --template-file "$BUILD_TEMPLATE" --stack-name test-amadou-stack

echo "Déploiement terminé. Récupérez ApiUrl depuis la sortie ou CloudFormation Outputs."
