#!/usr/bin/bash

#OS_AUTH_URL=https://ayoungdevstack20.cloudlab.freeipa.org/keystone/krb
OS_PROJECT_NAME=demo
OS_AUTH_URL=https://ayoungf20packstack.cloudlab.freeipa.org/keystone/krb

curl   \
-H "Content-Type:application/json" \
--negotiate -u : \
--cacert ca.crt  \
-i \
-d  '{ "auth": { "identity": { "methods": ["external"], "external": {}}, "scope": { "project": { "domain": { "name": "Default" }, "name": "demo" } } } }' \
-X POST $OS_AUTH_URL/v3/auth/tokens 
#| awk '/X-Subject-Token/ {print $2}'




