#!/usr/bin/bash
curl  -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" http://localhost:35357/v3/projects  | python -mjson.tool
