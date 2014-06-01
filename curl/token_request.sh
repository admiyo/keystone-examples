#!/usr/bin/bash

export TOKEN=`curl -si -d @token-request.json -H "Content-type: application/json" http://localhost:35357/v3/auth/tokens | awk '/X-Subject-Token/ {print $2}'` 
