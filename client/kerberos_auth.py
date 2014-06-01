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

import os

from keystoneclient import session
from keystoneclient.contrib.auth.v3 import kerberos

try:
    OS_AUTH_URL = os.environ['OS_AUTH_URL']
except KeyError as e:
    raise SystemExit('%s environment variables not set.' % e.message)

OS_CACERT = os.environ.get('OS_CACERT')
kerb_auth = kerberos.Kerberos(OS_AUTH_URL)
sess=session.Session(kerb_auth, verify=OS_CACERT)
token=sess.get_token()
print (token)