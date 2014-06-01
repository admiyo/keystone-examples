#!/usr/bin/bash
curl -si -H"X-Auth-Token:$TOKEN" -H "Content-type: application/json" http://localhost:35357/v3/projects -d @create_project.json
