import markdown
import yaml
import git_utils
import logging
from datetime import datetime, timedelta

md = None
def initMd():
    global md
    if md is None:
        md = markdown.Markdown(extensions = ['full_yaml_metadata'])

def extractMeta(fullname):
    file = open(fullname, 'r')
    data = file.read()
    file.close()

    initMd()
    try:
        md.convert(data)
    except ValueError:
        return None
    else:
        return md.Meta

def extractData(fullname):
    file = open(fullname, 'r')
    lines = file.readlines()
    try:
        lines.index('---\n')
    except ValueError:
        return ''.join([str(line) for line in lines])
    else:
        del lines[0]
        mark = lines.index('---\n')
        lines = lines[mark+1:]
        data = ''.join([str(line) for line in lines])
        return data

def readDate(date):
    if isinstance(date, str) or date is None:
        return date

    if isinstance(date, datetime):
        return date.isoformat()

def shouldUpdateModifyDate(meta_date, actual_date, edge_date, update_gap):
    if (
        edge_date and
        datetime.fromisoformat(meta_date) <= datetime.fromisoformat(edge_date)
    ):
        return False

    diff = abs(datetime.fromisoformat(meta_date) - datetime.fromisoformat(actual_date))
    logging.debug('Diff: ' + str(diff))
    return diff > timedelta(seconds=update_gap)

def writeMeta(repo_path, file_path, edge_date, update_gap):
    date_modified = git_utils.get_modify_date(repo_path, file_path)
    logging.debug('Git date: ' + date_modified)
    meta = extractMeta(file_path)
    should_write_meta = False

    if meta is None:
        meta = {}

    meta_date_created = readDate(meta.get('created'))
    meta_date_modified = readDate(meta.get('modified'))

    logging.debug('File date: ' + str(meta_date_modified))

    if (meta_date_created is None) or (meta_date_created) == '':
        should_write_meta = True
        meta['created'] = date_modified
        logging.debug('Add created to meta')
    else:
        meta['created'] = meta_date_created

    if (
        (meta_date_modified is None) or
        shouldUpdateModifyDate(meta_date_modified, date_modified, edge_date, update_gap)
    ):
        should_write_meta = True
        meta['modified'] = date_modified
        logging.debug('Add modified to meta')
    else:
        meta['modified'] = date_modified

    if should_write_meta:
        logging.info('update meta for ' + file_path)
        data = extractData(file_path)
        file = open(file_path, 'w')
        file.write('---\n')
        yaml.dump(meta, file)
        file.write('---\n\n')
        file.write(data)
        file.close()

    return should_write_meta
