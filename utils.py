# coding=utf-8
import os
from time import time
from datetime import date
import easywebdav


def cleanDir(path, ttl):
    now = time()

    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if os.stat(fpath).st_mtime < now - ttl:
            os.remove(fpath)


def sortFile(dirname, reverse=True):
    dirlist = os.listdir(dirname)
    return sorted(dirlist, key=lambda x: os.lstat(x).st_mtime, reverse=reverse)


def sendToRemote(dirname, url, baseurl=None, username="anonimous", password="anonimous", scheduled="6"):
    today = date.today()
    if str(today.weekday()) not in scheduled:
        return

    fname = sortFile(dirname)[0]
    client = easywebdav.connect(url, username=username, password=password)
    if baseurl is not None:
        client.baseurl = baseurl
    try:
        client.upload(fname, fname)
    except easywebdav.WebdavException as e:
        pass
