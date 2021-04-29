import markdown
import os
import time
import datetime
import yaml
import re

pattern = re.compile(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\+03:00')

def convertDateToSec(date):
    return time.mktime(datetime.datetime.strptime(date, '%Y-%m-%dT%X%z')\
        .timetuple())

def extractMeta(fullname):
    file = open(fullname, 'r')
    data = file.read()
    file.close()
    md = markdown.Markdown(extensions = ['full_yaml_metadata'])
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

def writeMeta(fullname):
    meta = extractMeta(fullname)
    if meta is None:
        meta = {}
    if ((meta.get('created') is None) or
        (meta['created'] is None) or
        (meta['created'] == '')):
            meta['created'] = datetime.datetime\
                .fromtimestamp(os.stat(fullname).st_mtime)\
                .replace(microsecond=0).astimezone().isoformat()
    if ((meta.get('modified') is None) or
        (meta['modified'] is None) or
        (convertDateToSec(meta['modified']) <=
            (os.stat(fullname).st_mtime-10))):
                meta['modified'] = datetime.datetime\
                    .fromtimestamp(os.stat(fullname).st_mtime)\
                    .replace(microsecond=0).astimezone().isoformat()
                data = extractData(fullname) 
                file = open(fullname, 'w')
                file.write('---\n')
                yaml.dump(meta, file)
                file.write('---\n')
                file.write(data)
                file.close()
