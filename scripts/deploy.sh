#!/bin/bash
# Deployment script for git-camus

set -euo pipefail

ENVIRONMENT=${1:-dev}
NAMESPACE=${2:-git-camus}

echo "🚀 Deploying git-camus to $ENVIRONMENT environment..."

case $ENVIRONMENT in
  "dev")
    VALUES_FILE="helm/values-dev.yaml"
    ;;
  "prod")
    VALUES_FILE="helm/values-prod.yaml"
    ;;
  *)
    VALUES_FILE="helm/values.yaml"
    ;;
esac

# Validate Helm chart
echo "Validating Helm chart..."
helm lint helm/

# Check if namespace exists, create if not
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
    echo "Creating namespace $NAMESPACE..."
    kubectl create namespace "$NAMESPACE"
fi

# Deploy with Helm
echo "Deploying with Helm..."
helm upgrade --install git-camus helm/ \
    --namespace "$NAMESPACE" \
    --values "$VALUES_FILE" \
    --wait \
    --timeout=600s

# Verify deployment
echo "Verifying deployment..."
kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=git-camus

echo "✅ Deployment completed successfully!"
echo "🌐 Service endpoints:"
kubectl get svc -n "$NAMESPACE"