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

from keystoneclient import exceptions
from keystoneclient.v3 import client

try:
    OS_SERVICE_ENDPOINT = os.environ['OS_SERVICE_ENDPOINT']
    OS_SERVICE_TOKEN = os.environ['OS_SERVICE_TOKEN']
    #used for creating the ADMIN user
    OS_PASSWORD = os.environ['OS_PASSWORD']
    OS_USERNAME = os.environ['OS_USERNAME']
    OS_AUTH_URL = os.environ['OS_AUTH_URL']
    OS_PROJECT_NAME = os.environ['OS_PROJECT_NAME']
except KeyError as e:
    raise SystemExit('%s environment variables not set.' % e.message)


def build_admin_user(admin_client):
    """The end state: admin user is created with the appropriate roles in the
    admin project to perform administrative tasks.
    """
    #default domain already exists
    default_domain = admin_client.domains.list(id='default')[0]

    try:
        admin_client.projects.create(
            name=OS_PROJECT_NAME, domain=default_domain.id,
            description='For Administrative Actions Only')
    except exceptions.Conflict:
        #default domain is likely to be created already
        pass

    admin_project = admin_client.projects.list(name=OS_PROJECT_NAME,
                                               domain=default_domain.id)[0]
    admin_client.users.create(name=OS_USERNAME,
                              domain=default_domain.id,
                              default_project=admin_project.id,
                              password=OS_PASSWORD)
    admin_client.roles.create(name='admin')
    admin_user = admin_client.users.list(name='admin',
                                         domain='default')[0]
    admin_role = admin_client.roles.list(name='admin')[0]
    admin_client.roles.grant(role=admin_role.id,
                             user=admin_user.id,
                             domain=default_domain.id)
    admin_client.roles.grant(role=admin_role.id,
                             user=admin_user.id,
                             project=admin_project.id)


def build_service_catalog(admin_client):
    admin_client.services.create(name='Keystone',
                                 type='identity')
    identity_service = admin_client.services.list(name='Keystone',
                                                  type='identity')[0]
    for interface in ['public', 'admin', 'internal']:
        admin_client.endpoints.create(
            identity_service.id,
            url='http://localhost:35357/v3',
            interface=interface)


def client_for_admin_user():
    admin_client = client.Client(auth_url=OS_AUTH_URL,
                                 management_url=OS_SERVICE_ENDPOINT,
                                 username=OS_USERNAME,
                                 password=OS_PASSWORD,
                                 project_name=OS_PROJECT_NAME,
                                 debug=True)
    return admin_client


def initialize():
    admin_client = client.Client(endpoint=OS_SERVICE_ENDPOINT,
                                 token=OS_SERVICE_TOKEN)
    build_admin_user(admin_client)
    build_service_catalog(admin_client)
    admin_user_client = client_for_admin_user()
    print("client created for %s" % admin_user_client.username)

if __name__ == '__main__':
    initialize()
