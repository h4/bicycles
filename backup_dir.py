#!/usr/bin/env python
# coding=utf-8

"""
Скрипт резервного копирования каталога

Ключи
-d --dir        - каталог с резервными копиями
-n --filename   - имя файла резервной копии
"""

import argparse
import tarfile
from datetime import datetime


def backup(source, target, filename):
    dt = datetime.today().strftime('%Y_%m_%d')

    fname = '{}/{}__{}.tar.gz'.format(target, filename, dt)

    try:
        archive = tarfile.open(fname, "w:gz")
        archive.add(source)
        archive.close()
    except tarfile.TarError as e:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Directory backup utility')

    parser.add_argument('-d', '--dir', help='path to backups')
    parser.add_argument('-n', '--filename', help='backup file name')
    parser.add_argument('source', help='sources directory')

    args = parser.parse_args()

    backup(args.source, args.dir, args.filename)
