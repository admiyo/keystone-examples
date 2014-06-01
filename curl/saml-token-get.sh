#!/usr/bin/bash
curl  \
-H "Content-Type:application/json" \
--negotiate -u : \
--cacert ca.crt  \
-d  '{ "auth": { "identity": { "methods": ["saml2"], "saml2":{"identity_provider":"sssd", "protocol":"kerberos"}}, "scope": { "project": { "domain": { "name": "Default" }, "name": "Castle" } } } }' \
-X POST https://ayoungdevstack20.cloudlab.freeipa.org/keystone/sss/v3/auth/tokens




