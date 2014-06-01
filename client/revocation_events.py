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
import time

from keystoneclient.common import cms
from keystoneclient.openstack.common import jsonutils
from keystoneclient.v3 import client

#assumes initialize_keystone.py has been run.

#usernames randomly selected from a list of on the most popular last names
usernames = ['astanley', 'chess', 'cli',
             'mstevens', 'ofox', 'odunn',
             'ohart', 'pray', 'qlane',
             'rsilva', 'rcraig', 'sleonard']


def add_users(admin_client, test_domain, role, projects):
    for name in usernames:
        user = admin_client.users.create(name=name, password=name,
                                         domain=test_domain)
        for project in projects:
            admin_client.roles.grant(role=role,
                                     user=user,
                                     project=project)


def remove_users(admin_client, test_domain):
    test_role = admin_client.roles.list(name='testrole')[0]
    test_projects = admin_client.projects.list(domain=test_domain)
    for user in admin_client.users.list(domain=test_domain):
        for project in test_projects:
            admin_client.roles.revoke(role=test_role,
                                      user=user,
                                      project=project)
        admin_client.users.delete(user.id)


def create_entities(admin_client):
    test_domain = admin_client.domains.create(name='TestDomain')
    projects = []
    for project_index in range(0, 3):
        projects.append(
            admin_client.projects.create(name='project_%d' % project_index,
                                         domain=test_domain))
    role = admin_client.roles.create('testrole')

    add_users(admin_client, test_domain, role, projects)

    return test_domain


def remove_projects(admin_client, test_domain):
    for project in admin_client.projects.list(domain=test_domain):
        admin_client.projects.delete(project=project)


def get_token_for_user_and_project(test_domain, test_project, test_user):
    user_client = (
        client.Client(auth_url='http://localhost:5000/v3',
                      management_url='http://localhost:35357/v3',
                      user_id=test_user.id,
                      user_domain_id=test_domain.id,
                      password=test_user.name,
                      project_id=test_project.id,
                      project_domain_id=test_domain.id))
    token = user_client.auth_ref['auth_token']
    user_token = jsonutils.loads(
        cms.verify_token(
            token,
            '/etc/keystone/ssl/certs/signing_cert.pem',
            '/etc/keystone/ssl/certs/ca.pem'))
    return user_token


def assert_not_revoked(admin_client, user_token):
    time.sleep(5)
    admin_client.revocations.synchronize()
    if admin_client.revocations.is_revoked(user_token):
        print("FAIL: token is revoked")
    else:
        print("OK  : token is valid")


def assert_revoked(admin_client, user_token):
    time.sleep(5)
    admin_client.revocations.synchronize()
    if admin_client.revocations.is_revoked(user_token):
        print("OK    : token is revoked")
    else:
        print("FAIL: token is valid")


def test_revoking_role(admin_client, test_domain, test_project, test_role):
    test_user = admin_client.users.list(name='rcraig', domain=test_domain)[0]
    print('testing tokens for %s ' % test_user.name)
    user_token = get_token_for_user_and_project(test_domain, test_project,
                                                test_user)
    assert_not_revoked(admin_client, user_token)
    admin_client.roles.revoke(role=test_role,
                              user=test_user,
                              project=test_project)
    assert_revoked(admin_client, user_token)


def test_deleting_project(admin_client, test_domain, test_project):
    test_user = admin_client.users.list(name='ofox', domain=test_domain)[0]
    print('testing tokens for %s ' % test_user.name)
    user_token = get_token_for_user_and_project(test_domain, test_project,
                                                test_user)
    assert_not_revoked(admin_client, user_token)
    admin_client.projects.delete(project=test_project)
    assert_revoked(admin_client, user_token)


def test_deleting_user(admin_client, test_domain, test_project):
    test_user = admin_client.users.list(name='ohart', domain=test_domain)[0]
    print('testing tokens for %s ' % test_user.name)
    user_token = get_token_for_user_and_project(test_domain, test_project,
                                                test_user)
    assert_not_revoked(admin_client, user_token)
    admin_client.users.delete(user=test_user)
    assert_revoked(admin_client, user_token)


def main():
    management_url = 'http://localhost:35357/v3'
    admin_client = client.Client(endpoint=management_url, token='freeipa4all')

    create_entities(admin_client)
    test_domain = admin_client.domains.list(name='TestDomain')[0]
    test_role = admin_client.roles.list(name='testrole')[0]
    test_project = admin_client.projects.list(name='project_1')[0]

    test_deleting_user(admin_client, test_domain, test_project)
    test_revoking_role(admin_client, test_domain, test_project, test_role)
    test_deleting_project(admin_client, test_domain, test_project)

    remove_users(admin_client, test_domain)
    admin_client.roles.delete(test_role)
    remove_projects(admin_client, test_domain)
    admin_client.domains.update(domain=test_domain, enabled=False)
    admin_client.domains.delete(domain=test_domain)

main()
