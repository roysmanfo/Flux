"""
# `cr observer`
"""

from watchdog.observers import Observer
import os

BUCKET_PATH: str = "\\".join([os.path.expanduser('~'), "Desktop", "Bucket"])

os.makedirs(BUCKET_PATH)
print(BUCKET_PATH)