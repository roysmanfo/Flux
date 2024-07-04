"""

Gather some statistic data about the repository like:
- number of lines of code
- number of files
- percentage of file of the same language language


"""

import os

_root = os.path.dirname(os.path.realpath(__file__))

scan_dirs = [ i for i in os.listdir(_root) if os.path.isdir(i)]
scan_ext = {}

# filters (if these are empty, the scan will include everything)
exclude_dirs = { 
    '.git',
    '.github',
    ".pytest_cache",
    ".venv",
    ".vscode",
    "docs",
    "img",
    }
exclude_ext = { ".pyc" }

# stats
c_files = { e:0 for e in scan_ext}
n_files = 0
n_lines = 0

# parse

scan_dirs = set(filter(lambda d: d not in exclude_dirs, scan_dirs))
scan_ext = set(filter(lambda d: d not in exclude_ext, scan_ext))

# data gathering
for path in scan_dirs: # filter out some folders
    for dirpath, _, files in os.walk(path):

        for file in files:
            ext = os.path.splitext(file)[1]
            if (not scan_ext and ext not in exclude_ext) or ext not in exclude_ext:
                n_files += 1
                c_files.update({ext: c_files.get(ext, 0) + 1})
                
                with open(os.path.join(dirpath, file), "rb") as f:
                    n_lines += len(f.readlines())


print("num files:", n_files)
print("num lines:", n_lines)
print("\nlanguages:")

for ext, num in sorted(c_files.items(), key=lambda x: x[0]):
    lang = f'{ext or 'no_extension'} ({num})'
    print(f" - {lang:30}{round(num / n_files * 100)}%")

print()