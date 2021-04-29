import argparse
import walker
import md_work
import os

path = '/home/boohmax/work/note-taker/'

'''parser = argparse.ArgumentParser("""Note-taker""")
parser.add_argument('--path', type=str, help='Write path')
args = parser.parse_args()'''

base_md_file = {}

for file in walker.collectFile(path):
    md_work.writeMeta(file)

for file in walker.collectFile(path):
    base_md_file[file] = md_work.extractMeta(file)

for key, value in base_md_file.items():
    print(key, '\n',value)
