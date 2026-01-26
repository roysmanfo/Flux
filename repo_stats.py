"""

Gather some statistic data about the repository like:
- number of lines of code
- number of files
- percentage of file of the same language language


"""

import os

_root = os.path.dirname(os.path.realpath(__file__))

# scan_dirs = [ i for i in os.listdir(_root) if os.path.isdir(i)]
scan_ext = { ".py", "", ".sh" }

scan_dirs = {
    'flux',
    'tests',
}

# stats
c_files = { e:0 for e in scan_ext}
n_files = 0
n_lines = 0
total_size = 0
# parse

# scan_dirs = set(filter(lambda d: d in include_dirs, scan_dirs))
# scan_ext = set(filter(lambda d: d in include_ext, scan_ext))

# data gathering
for path in scan_dirs: # filter out some folders
    for dirpath, _, files in os.walk(path):

        for file in files:
            ext = os.path.splitext(file)[1]
            if (scan_ext and ext in scan_ext):
                n_files += 1
                c_files.update({ext: c_files.get(ext, 0) + 1})

                with open(os.path.join(dirpath, file), "rb") as f:
                    n_lines += len(f.readlines())
                    total_size += os.stat(os.path.join(dirpath, file)).st_size


print("num files:", n_files)
print("num lines:", n_lines)
print("\nlanguages:")

for ext, num in sorted(c_files.items(), key=lambda x: x[0]):
    lang = f"{ext or 'no_extension'} ({num})"
    print(f" - {lang:30}{(num / n_files * 100):-5.1f}%")

units = ('B', 'kB', 'MB', 'GB')
i = 0
limit = 1024
while total_size > limit:
    if i == len(units):
        break
    total_size /= limit
    i+=1

print(f"\nTotal codebase size: {total_size:.2f}{units[i]}")
print()
