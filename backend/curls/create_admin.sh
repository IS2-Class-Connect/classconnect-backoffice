#!/bin/sh

if [ $# -ne 1 ]; then
    echo "use: $0 <username:string>"
    exit 1
fi

curl -X 'POST' \
  'http://localhost:3004/admins/create' \
  -H 'Content-Type: application/json' \
  -d "{
    \"username\": \"$1\",
    \"email\": \"$1@example.com\",
    \"password\": \"securepassword\"
  }"

