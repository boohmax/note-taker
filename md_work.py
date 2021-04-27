import markdown
import os
import time
import yaml
import re

pattern = re.compile(r'\d\d\d\d-\d\d-\d\d T\d\d:\d\d:\d\d \+0300')

def convertDateToSec(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d T%X %z'))

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

def metaCreated(fullname):
    meta = extractMeta(fullname)
    if meta is None:
        meta = {}
    if ((meta.get('created') is None) or
        (meta['created'] is None) or
        (meta['created'] == '') or
        (pattern.fullmatch(meta['created']) == None)):
            data = extractData(fullname)
            meta['created'] = time.strftime(
                '%Y-%m-%d T%X %z', time.localtime(os.stat(fullname).st_mtime)
                )
            file = open(fullname, 'w')
            file.write('---\n')
            yaml.dump(meta, file)
            file.write('---\n')
            file.write(data)
            file.close()

def metaModified(fullname):
    meta = extractMeta(fullname)
    if ((meta.get('modified') is None) or
        (meta['modified'] is None) or
        (convertDateToSec(meta['modified'])
            <= (os.stat(fullname).st_mtime-10))):
                data = extractData(fullname)
                meta['modified'] = str(time.strftime('%Y-%m-%d T%X %z',
                    time.localtime(os.stat(fullname).st_mtime)))
                file = open(fullname, 'w')
                file.write('---\n')
                yaml.dump(meta, file)
                file.write('---\n')
                file.write(data)
                file.close()