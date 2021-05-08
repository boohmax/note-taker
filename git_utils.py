import subprocess

def get_modify_date(repo_path, file_path):
    date_modified = subprocess.run([
        'git', '-C', repo_path,
        'log', '-1', '--format=%cI', '--',
        file_path
        ], stdout=subprocess.PIPE, text=True).stdout.strip('\n')
    return date_modified
