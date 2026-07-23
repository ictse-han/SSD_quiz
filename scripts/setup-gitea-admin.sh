#!/bin/bash
# Run this once after `docker compose up -d gitea` has finished starting.
# Satisfies Q1: username "admin", password 2301483@sit.singaporetech.edu.sg
set -e

docker exec -u git gitea gitea admin user create \
  --username admin \
  --password '2301483@sit.singaporetech.edu.sg' \
  --email 2301483@sit.singaporetech.edu.sg \
  --admin \
  --must-change-password=false

echo "Gitea admin account created. Log in at http://localhost:3000"
