from collections import defaultdict
import os

ignore = [
    '.DS_Store',
    '__pycache__',
    'node_modules',
    '.git',
    '.venv',
    '.png',
    '.ico',
    '.jpg',
    '.json',
    'pip.lock',
    'pnpm-lock.yaml',
    'yarn.lock',
    'market_data/',
    'build/'
]


def check_ignore(path):
    return all(x not in path for x in ignore)


def iterate_all_files_recursively(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            if check_ignore(path):
                yield path


def read_line_count(path):
    with open(path, 'r', encoding='utf8') as f:
        return sum(1 for line in f)


def read_all_line_counts(files):
    counts = []
    for f in files:
        counts.append(read_line_count(f))
    return counts


if __name__ == '__main__':
    files = []
    for i in iterate_all_files_recursively('.'):
        files.append(i)
    count = len(files)
    line_counts = read_all_line_counts(files)

    print(f"File count: {count}")
    print(f"Line count: {sum(line_counts)}")

    # Calculate folder stats
    folderdict = defaultdict({'files': 0, 'lines': 0}.copy)
    for i, f in enumerate(files):
        parts = f.split('/')
        if len(parts) == 2:
            folderdict['<root>']['files'] += 1
            folderdict['<root>']['lines'] += line_counts[i]
        else:
            folder = parts[1]
            folderdict[folder]['files'] += 1
            folderdict[folder]['lines'] += line_counts[i]
    
    print("Folder stats:")
    for k, v in folderdict.items():
        print(f"   {k}: {v['files']} files, {v['lines']} lines")