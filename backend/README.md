# Backend (Python / FastAPI)

Prerequisites:
- Python 3.11
- AWS SAM CLI (for local build/deploy)

Local install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Déployer avec SAM (interactive):

```bash
sam build -t ../infra/template.yaml
sam deploy --guided
```

Le template SAM provisionne une table DynamoDB et une fonction Lambda exposée par API Gateway.
