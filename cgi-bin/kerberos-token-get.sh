#!/usr/bin/bash



OS_AUTH_URL=https://ayoungf20packstack.cloudlab.freeipa.org/keystone/krb
OS_PROJECT_NAME=demo


TOKEN=`curl   \
-H "Content-Type:application/json" \
--negotiate -u : \
-d  '{ "auth": { "identity": { "methods": []}, "scope": { "project": { "domain": { "name": "Default" }, "name": "demo" } } } }' \
-X POST $OS_AUTH_URL/v3/auth/tokens   `

#!/bin/bash

echo "Content-type: application/json"
echo ""

echo $TOKEN 

exit 0

