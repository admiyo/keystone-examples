#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Example of manipulating Regions using the client and the V3 API.

Performs Create without and with parent region, list, update and delete.

Uses the OS_SERVICE_TOKEN to authenticate, assuming a new install and no
established authentication information.

"""
from __future__ import print_function

import os
import sys

from keystoneclient.v3 import client

try:
    OS_SERVICE_ENDPOINT = os.environ['OS_SERVICE_ENDPOINT']
    OS_SERVICE_TOKEN = os.environ['OS_SERVICE_TOKEN']
except KeyError as e:
    print ('%s environment variables not set.' % e.message,
           file=sys.stderr)
    exit(1)


admin_client = client.Client(endpoint=OS_SERVICE_ENDPOINT,
                             token='freeipa4all')

admin_client.regions.create(id='Australia',
                            description="The Island Continent")
admin_client.regions.get('Australia')

NSW = admin_client.regions.create(id='NSW',
                                  description='New South Wales',
                                  parent_region='Australia')

Sydney = admin_client.regions.create(id='Sydney',
                                     description='More than an Opera House',
                                     parent_region=NSW)

Oceana = admin_client.regions.create(
    id='Oceana', description='Places south and east of Asia')

admin_client.regions.update('Australia', parent_region=Oceana,
                            description='The Island Continent Country')

for region in admin_client.regions.list():
    print("id = %s, parent = %s, description=%s" % (
        region.id, region.parent_region_id, region.description))

admin_client.regions.delete('Sydney')
admin_client.regions.delete('NSW')
admin_client.regions.delete('Australia')
admin_client.regions.delete('Oceana')
