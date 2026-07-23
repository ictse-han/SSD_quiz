#!/bin/bash
# Usage: ./scripts/sonar-scan.sh <sonar-token>
# Generate the token first: log in to http://127.0.0.1:9000 -> My Account -> Security -> Generate Token
set -e

TOKEN="$1"
if [ -z "$TOKEN" ]; then
  echo "Usage: $0 <sonar-token>"
  exit 1
fi

docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="$TOKEN" \
  -v "$(pwd)/web:/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=secure-login-app \
  -Dsonar.sources=.
