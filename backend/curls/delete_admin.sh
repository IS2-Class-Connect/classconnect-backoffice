#!/bin/sh

if [ $# -ne 1 ]; then
    echo "use: $0 <id:string>"
    exit 1
fi

curl -X DELETE \
  "http://localhost:3004/admins/$1" \
  -H 'Content-Type: application/json'

