# coding=utf-8

import yaml
import argparse
import utils
import backup_db
import backup_dir


class Backup(object):
    def __init__(self, config_file):
        f = open(config_file)
        self.config = yaml.load(f.read())

    def run(self):
        if "directories" in self.config:
            self.backup_dir()
        if "databases" in self.config:
            self.backup_db()

    def backup_db(self):
        databases = self.config['databases']
        for db in databases:
            db_name = db.keys()[0]
            params = db.values()[0]
            try:
                backup_db.backup(db_name, params['dir'], params['user'], params['password'])
                self.sentToRemote(params['dir'])
            finally:
                ttl = params.setdefault('ttl', self.config['ttl'])
                utils.cleanDir(params['dir'], ttl)

    def backup_dir(self):
        paths = self.config['directories']
        for path in paths:
            params = path.values()[0]
            backup = backup_dir.backup(params['source'], params['target'], params['backup_name'])
            ttl = params.setdefault('ttl', self.config['ttl'])
            utils.cleanDir(params['target'], ttl)
            if backup is not None:
                self.sentToRemote(params['target'])

    def sentToRemote(self, dirname):
        if "remotes" not in self.config:
            return
        for remote in self.config['remotes']:
            params = remote.values()[0]
            if params['type'] == 'webdav':
                self._webdavSync(dirname, params)

    @staticmethod
    def _webdavSync(dirname, params):
        utils.sendToRemote(dirname, params['url'], username=params['username'],
                           password=params['password'], scheduled=params['schedule'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backup utility')

    parser.add_argument('config', help='path to configuration file')
    args = parser.parse_args()

    Backup(args.config).run()
