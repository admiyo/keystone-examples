#!/usr/bin/bash
export TOKEN=freeipa4all
curl  -H"X-Auth-Token:$TOKEN" http://localhost:35357/v3/projects |  jq '.projects[] | {id, name}  '
