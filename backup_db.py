#!/usr/bin/env python
# coding=utf-8

"""
Скрипт резервного копирования базы данных

python backup_db.py [OPTIONS] database

Ключи
-d --dir        - каталог с резервными копиями
-u --username   - имя пользователя бд
-p --password   - пароль бд
"""

import argparse
import gzip
import subprocess
from datetime import datetime

def backup(database, target, username, password):
    mysql_cmd = ['mysqldump', '--user=' + username, '--password=' + password, database]
    mysql_proc = subprocess.Popen(mysql_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    mysql_out = mysql_proc.communicate()[0]

    dt = datetime.today().strftime('%Y_%m_%d')

    fname = '{}/{}__{}.gz'.format(target, database, dt)

    f = gzip.open(fname, 'wb')
    f.write(mysql_out)
    f.close()
    return fname

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MySQL backup utility')

    parser.add_argument('-u', '--username', help='database user name')
    parser.add_argument('-p', '--password', help='database password')
    parser.add_argument('-d', '--dir', help='backups dir')
    parser.add_argument('database', help='database name')

    args = parser.parse_args()

    backup(args.database, args.dir, args.username, args.password)
