#!/bin/bash
set -e

FILE="/docker-entrypoint-initdb.d/data/100k-most-used-passwords-NCSC.txt"

if [ -f "$FILE" ]; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    -c "\\COPY common_passwords(password) FROM '$FILE' WITH (FORMAT text)"
  echo "Loaded common password list into common_passwords."
else
  echo "WARNING: $FILE not found -- common_passwords table will be empty."
  echo "Download it before starting the stack (see QUIZ_NOTES.md step 0)."
fi
