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

from keystoneclient.v3 import client


try:
    OS_SERVICE_ENDPOINT = os.environ['OS_SERVICE_ENDPOINT']
    OS_SERVICE_TOKEN = os.environ['OS_SERVICE_TOKEN']
except KeyError as e:
    raise SystemExit('%s environment variables not set.' % e.message)


def tear_down_service_catalog(admin_client):
    for endpoint in admin_client.endpoints.list():
        admin_client.endpoints.delete(endpoint.id)

    for service in admin_client.services.list():
        admin_client.services.delete(service.id)


def tear_down_data(admin_client):
    for domain in admin_client.domains.list():
        if domain.id == 'default':
            continue
        for project in admin_client.projects.list(domain):
            admin_client.projects.delete(project)
        for user in admin_client.users.list(domain):
            admin_client.users.delete(user)
        admin_client.domains.update(domain, enabled=False)
        admin_client.domains.delete(domain)


def tear_down_admin_user(admin_client):
    admin_user = admin_client.users.list(name='admin')[0]
    admin_project = admin_client.projects.list(name='admin',
                                               domain='default')[0]
    default_domain = admin_client.domains.get('default')

    for admin_role in admin_client.roles.list(name='admin'):
        admin_client.roles.revoke(role=admin_role,
                                  user=admin_user,
                                  project=admin_project)
        admin_client.roles.revoke(role=admin_role,
                                  user=admin_user,
                                  domain=default_domain)
    admin_client.users.delete(admin_user)
    admin_client.projects.delete(admin_project)


def main():
    management_url = OS_SERVICE_ENDPOINT
    admin_client = client.Client(endpoint=management_url,
                                 token=OS_SERVICE_TOKEN)

    tear_down_data(admin_client)
    tear_down_service_catalog(admin_client)
    try:
        tear_down_admin_user(admin_client)
    except IndexError:
        pass
    for role in admin_client.roles.list():
        admin_client.roles.delete(role)

if __name__ == '__main__':
    main()
