import os
import shutil
import subprocess
import pwd
from tornado import gen
from  ldapauthenticator import LDAPAuthenticator
import getpass


class KDBAuthenticator(LDAPAuthenticator):
"""
Позволяет проходить аутентифицацию по LDAP и привязывать сертификат kerberos к пользователю.
Далее можно получать доступ к БД MS SQL (через настройку odbc драйвера), который поддерживает kerberos авторизацию. 
Аторизация проходить при втором подключении, так как при первой авторизации, будет создан пользователь.
"""
    @gen.coroutine
    def authenticate(self, handler, data):
        ans = yield super().authenticate(handler, data)
        if ans is not None:
            try:
                user = data.get('username', 'None').lower()
                self.log.info('Authenticating: ' + user)
                pwrd = data['password']
                #Получаем идентификатор целевого пользователя
                target_user=pwd.getpwnam(user).pw_uid
                owner_user = os.getuid()
                #Формируем вызов комманды, для получения сертификата
                realm = '######.RU'
                kinit = '/usr/bin/kinit'
                kuser = '%s@%s' % (user, realm)
                krbcc ='/tmp/krb5cc_{uid}'.format(uid=str(target_user))

                kinit_args = [kinit, kuser, '-c', krbcc]
                pecho_args = ['echo', '-n', pwrd]
                self.log.warning('Running: ' + ' '.join(kinit_args))
                self.log.warning('Running #####################: '+ str(os.getuid()))
                #Подменяем пользователя, от имени которого будет выполняться получение сетификата
                os.seteuid(target_user)
                pecho = subprocess.Popen(pecho_args, stdout=subprocess.PIPE)
                kinit = subprocess.Popen(kinit_args, stdin=pecho.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #Поменяем обратно на root пользователя и продолжим выполнение
                os.seteuid(0)
                self.log.info(kinit.communicate())
                return user
            except  Exception as e:
                return user
        return None
