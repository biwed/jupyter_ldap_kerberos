import os
import psycopg2

import sys
# Путь до kdba_authenticator
sys.path.insert(0, '/srv/jupyterhub/')

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8889
c.JupyterHub.port = 8888
c.Spawner.default_url = '/lab'

c.Spawner.environment = {
 'RES_PG_LOGIN': '#####',
}

c.JupyterHub.authenticator_class = 'kdba_authenticator.KDBAuthenticator'
c.LDAPAuthenticator.server_hosts = ['ldap.########.ru']
c.LDAPAuthenticator.server_port = 3268
c.LDAPAuthenticator.bind_user_dn = 'cn=######,ou=_System accounts and groups,ou=#######,dc=########,dc=ru'
c.LDAPAuthenticator.bind_user_password = '#########'
c.LDAPAuthenticator.user_search_base = 'dc=########,dc=ru'
c.LDAPAuthenticator.user_search_filter = '(&(objectClass=person)(sAMAccountName={username}))'
c.LDAPAuthenticator.user_membership_attribute = 'memberOf'
c.LDAPAuthenticator.group_search_base = 'CN=Groups,DC=########,DC=ru'
c.LDAPAuthenticator.group_search_filter = '(&(objectClass=group)(memberOf={group}))'
c.LDAPAuthenticator.allowed_groups = [
 'CN=IT-группа анализа данных,OU=_ДолжностиИОтделы,OU=#######,DC=########,DC=ru',
 ]
c.LDAPAuthenticator.allow_nested_groups = True
c.LDAPAuthenticator.username_pattern = '[a-zA-Z0-9_.][a-zA-Z0-9_.-]{2,20}[a-zA-Z0-9_.$-]?'
c.LDAPAuthenticator.create_user_home_dir = True
c.Authenticator.delete_invalid_users = True
c.LDAPAuthenticator.create_user_home_dir_cmd = ['useradd','-s','/bin/bash','-m']

c.Authenticator.enable_auth_state = True