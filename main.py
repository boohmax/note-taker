import argparse
import walker
import md_work
import logging
from datetime import datetime

parser = argparse.ArgumentParser("""Note-taker""")
parser.add_argument('--path', required=True, type=str, help='Repository path')
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, help='Verbosity level')
parser.add_argument(
    '--edge-date',
    type=str,
    help='Date and time of commit after which files will be processed, ISO 8601 date-time string'
)
parser.add_argument(
    '--update-gap',
    type=int,
    default=30,
    help='Max delta between metadata update date and last channge commit date, seconds'
)
args = parser.parse_args()

verbose = args.verbose
if verbose:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Logger level set to DEBUG')
else:
    logging.basicConfig(level=logging.INFO)

path = args.path
logging.info('Repo path: ' + path)

edge_date = args.edge_date
if (edge_date):
    try:
        datetime.fromisoformat(edge_date)
    except Exception as e:
        logging.error('Cannot parse edge date: ' + e.args[0])
        exit(1)
    logging.info('Edge date: ' + str(edge_date))

update_gap = args.update_gap
logging.info('Update gap: ' + str(update_gap))

total_count = 0
updated_count = 0

for file in walker.collectFile(path):
    logging.debug('=== Process file: ' + file)

    total_count = total_count + 1
    if (md_work.writeMeta(path, file, edge_date, update_gap)):
        updated_count = updated_count + 1

logging.info('Updated: ' + str(updated_count) + ' / ' + str(total_count))
