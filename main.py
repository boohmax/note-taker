import argparse
import walker
import md_work
import logging

parser = argparse.ArgumentParser("""Note-taker""")
parser.add_argument('--path', required=True, type=str, help='Repository path')
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, help='Verbosity level')
args = parser.parse_args()

verbose = args.verbose
if verbose:
	logging.basicConfig(level=logging.DEBUG)
	logging.debug('Logger level set to DEBUG')
else:
	logging.basicConfig(level=logging.INFO)

path = args.path
logging.info('Repo path: ' + path)

for file in walker.collectFile(path):
    logging.debug('Process file: ' + path)

    md_work.writeMeta(path, file)
