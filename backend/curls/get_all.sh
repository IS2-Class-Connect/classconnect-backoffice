#!/bin/sh

curl -X GET http://localhost:3004/admins \
  -H 'accept: application/json'
