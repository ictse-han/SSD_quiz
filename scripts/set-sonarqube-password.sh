#!/bin/bash
# Run this once after `docker compose up -d sonarqube` has finished starting
# (check http://127.0.0.1:9000 is reachable first -- first boot takes a minute or two).
# SonarQube ships with default admin/admin; this rotates it to the required password.
set -e

NEW_PASSWORD='2301483@sit.singaporetech.edu.sg'

curl -u admin:admin -X POST \
  "http://127.0.0.1:9000/api/users/change_password" \
  -d "login=admin&password=${NEW_PASSWORD}&previousPassword=admin"

echo "SonarQube admin password set. Log in at http://127.0.0.1:9000 with admin / ${NEW_PASSWORD}"
echo "NOTE: SonarQube enforces a password policy (length/character mix.)"
echo "If this curl call fails with 400, the API rejected the password --"
echo "log in via the web UI once with admin/admin and set it manually there instead,"
echo "the UI will tell you exactly which rule failed."
