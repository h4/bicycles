#!/usr/bin/env python

import argparse
import gzip
import subprocess
from datetime import datetime

from utils import cleanDir

backups_ttl = 14 * 86400

parser = argparse.ArgumentParser(description='MySQL backup utility')

parser.add_argument('-u', '--username', help='database user name')
parser.add_argument('-p', '--password', help='database password')
parser.add_argument('-d', '--dir', help='backups dir')
parser.add_argument('database', help='database name')

args = parser.parse_args()

mysql_cmd = ['mysqldump', '--user=' + args.username, '--password=' + args.password, args.database] 
mysql_proc = subprocess.Popen(mysql_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
mysql_out = mysql_proc.communicate()[0]

dt = datetime.today().strftime('%Y_%m_%d')

fname = '{}/{}__{}.gz'.format(args.dir, args.database, dt)

f = gzip.open(fname, 'wb')
f.write(mysql_out)
f.close()

cleanDir(args.dir, backups_ttl)
