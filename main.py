import argparse
import walker
import md_work
import logging

logging.basicConfig(level=logging.INFO)

# path = '/home/boohmax/work/note-taker/fixtures/example-for-test'

parser = argparse.ArgumentParser("""Note-taker""")
parser.add_argument('--path', required=True, type=str, help='Repository path')
args = parser.parse_args()
path = args.path
logging.info('Repo path: ' + path)

for file in walker.collectFile(path):
    logging.debug(file)

    md_work.writeMeta(path, file)
