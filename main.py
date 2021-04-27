import argparse
import walker
import md_work
import os

path = '/home/boohmax/work/note-taker/'

'''parser = argparse.ArgumentParser("""Note-taker""")
parser.add_argument('--path', type=str, help='Write path')
args = parser.parse_args()'''

base = {}

for file in walker.collectFile(path):
    md_work.metaCreated(file)
    md_work.metaModified(file)


for file in walker.collectFile(path):
    base[file] = md_work.extractMeta(file)

for key, value in base.items():
    print(key, '\n',value)
    print(os.stat(key).st_mtime, md_work.convertDateToSec(value['modified']),
        os.stat(key).st_mtime <= md_work.convertDateToSec(value['modified'])+10,
        os.stat(key).st_mtime - (md_work.convertDateToSec(value['modified'])+10))
