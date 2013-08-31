# coding=utf-8
import os
from time import time


def cleanDir(path, ttl):
    now = time()

    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if os.stat(fpath).st_mtime < now - ttl:
            os.remove(fpath)
