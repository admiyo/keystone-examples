curl  -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" -d '{"domain": {"description": "--optional--", "enabled": true, "name": "dom1"}}'  http://localhost:35357/v3/domains
