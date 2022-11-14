"""
# `cr observer`

### Copyright notice

This files contains work from Kalle Hallden
https://github.com/KalleHallden/desktop_cleaner

MIT License

Copyright (c) 2019 kalle hallden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
from datetime import date
from pathlib import Path
from .helpers.extensions import extension_paths
from time import sleep
import asyncio


async def run(info: list, from_command_line: bool = False) -> None:
    if from_command_line:
        print("Observer running")
        print("Press Ctrl+C to stop")
        await sort_files(info)
        print("Observer stopped")
    else:
        await sort_files(info)


async def sort_files(info: list) -> None:
    watch_path = Path(info[1].bucket)
    destination_root = Path(info[1].bucket_destination)

    try:
        os.makedirs(watch_path)
    except FileExistsError:
        pass

    try:
        os.makedirs(destination_root)
    except FileExistsError:
        pass

    try:
        event_handler = EventHandler(
            watch_path=watch_path, destination_root=destination_root)

        observer = Observer()
        observer.schedule(event_handler, f'{watch_path}', recursive=True)
        observer.start()

        try:
            while True:
                await asyncio.sleep(.1)
                continue
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        return

    except FileNotFoundError:
        # We deleted one or both directories
        await sort_files(info)


def create_destination_path(path: Path) -> Path:
    """
    Helper function that adds current year/month to destination path. If the path
    doesn't already exist, it is created.
    :param Path path: destination root to append subdirectories based on date
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def rename_file(source: Path, destination_path: Path) -> Path:
    """
    Helper function that renames file to reflect new path. If a file of the same
    name already exists in the destination folder, the file name is numbered and
    incremented until the filename is unique (prevents overwriting files).
    :param Path source: source of file to be moved
    :param Path destination_path: path to destination directory
    """
    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / \
                f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name


class EventHandler(FileSystemEventHandler):
    """    
    When a file is moved in the bucket, the event handler detects it and
    moves it in the appropiate folder
    """

    def __init__(self, watch_path: Path, destination_root: Path) -> None:
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def restore_dirs(self) -> None:
        """    
        Will restore the bucket if it has been deleted after opening the app
        """
        os.makedirs(self.watch_path)

        os.makedirs(self.destination_root)

    def on_modified(self, event) -> None:
        self.restore_dirs()

        for child in self.watch_path.iterdir():

            # skips directories and non-specified extensions
            if child.is_file() and child.suffix.lower() in extension_paths:
                destination_path = self.destination_root / \
                    extension_paths[child.suffix.lower()]
                destination_path = create_destination_path(
                    path=destination_path)
                destination_path = rename_file(
                    source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)

            elif child.is_file() and child.suffix.lower() not in extension_paths:
                destination_path = self.destination_root / \
                    extension_paths["noname"]
                destination_path = create_destination_path(
                    path=destination_path)
                destination_path = rename_file(
                    source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)
