#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: $0 <email>"
    exit 1
fi

curl -X POST \
  'http://localhost:3004/admins/login' \
  -H 'Content-Type: application/json' \
  -d "{
    \"email\": \"$1\",
    \"password\": \"securepassword\"
  }"
