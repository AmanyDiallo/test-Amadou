#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/update_frontend_api_url.sh <API_URL>
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <API_URL>" >&2
  exit 2
fi

API_URL="$1"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND_HTML="$ROOT_DIR/frontend/index.html"

if [ ! -f "$FRONTEND_HTML" ]; then
  echo "Fichier frontend/index.html introuvable" >&2
  exit 1
fi

# Remplacer le placeholder
sed -i.bak "s|<API_URL_PLACEHOLDER>|${API_URL}|g" "$FRONTEND_HTML"
echo "Mise à jour effectuée dans $FRONTEND_HTML (backup saved as index.html.bak)"
