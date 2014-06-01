curl  -H"X-Auth-Token:$TOKEN" http://localhost:35357/v3/role_assignments?scope.project.id=e15bab932d9349f7b2cbe6f1ae62cc8c  |  jq '.role_assignments[] | {user, role} '
