#!/usr/bin/bash
curl -s  -H"X-Auth-Token:$TOKEN" http://localhost:35357/v3/roles | jq '.roles[] | select( contains({name: "usermanager"})) | {id}[]  '
