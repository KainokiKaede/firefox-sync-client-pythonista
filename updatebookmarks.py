import os
import json
from myclient import SyncSample

username = "ham@example.com"
password = "spam"
passphrase = "s-pamsp-amspa-mspam-spams-pamsp"

def update_bookmarks(filepath=os.path.join(os.environ['HOME'],'Documents','bookmarks.json')):
    s = SyncSample(username, password, passphrase)
    meta = s.get_meta()
    assert meta['storageVersion'] == 5
    out_file = open(filepath, 'w')
    json.dump(s.bookmarks_full(), out_file)
    out_file.close()

if __name__ == '__main__':
    update_bookmarks()
