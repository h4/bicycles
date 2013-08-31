#!/usr/bin/env python
# coding=utf-8

"""
Скрипт резервного копирования каталога

Файлы хранятся 14 дней
Ключи
-d --dir        - каталог с резервными копиями
-n --filename   - имя файла резервной копии
"""

import argparse
import tarfile
from datetime import datetime

from utils import cleanDir

backups_ttl = 14 * 86400

parser = argparse.ArgumentParser(description='Directory backup utility')

parser.add_argument('-d', '--dir', help='backups dir')
parser.add_argument('-n', '--filename', help='backup file name')
parser.add_argument('target', help='target directory')

args = parser.parse_args()

dt = datetime.today().strftime('%Y_%m_%d')

fname = '{}/{}__{}.tar.gz'.format(args.dir, args.filename, dt)

try:
    archive = tarfile.open(fname, "w:gz")
    archive.add(args.target)
    archive.close()
except tarfile.TarError as error:
    pass

cleanDir(args.dir, backups_ttl)
