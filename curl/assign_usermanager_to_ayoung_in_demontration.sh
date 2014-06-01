#!/usr/bin/bash

export USERMANAGER_ID=$(curl -s  -H"X-Auth-Token:$TOKEN" http://localhost:35357/v3/roles | jq '.roles[] | select( contains({name: "usermanager"})) | {id}[]  '  | sed 's!\"!!g' )
export AYOUNG_ID=$( curl -s  -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" http://localhost:35357/v3/users | jq '.users[] | select( contains ({name: "ayoung"})) | {id}[]  '| sed 's!\"!!g' )
export DEMONSTRATION_ID=$( curl -s  -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" http://localhost:35357/v3/projects | jq '.projects[] | select( contains({name: "Demonstration"})) | {id}[]  '     | sed 's!\"!!g'  )

#must be something better than SED above.

curl  -X PUT  -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" http://localhost:35357/v3/projects/$DEMONSTRATION_ID/users/$AYOUNG_ID/roles/$USERMANAGER_ID

curl  -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" http://localhost:35357/v3/projects/$DEMONSTRATION_ID/users/$AYOUNG_ID/roles | jq '.'
