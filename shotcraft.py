from __future__ import annotations

import argparse
import collections
import datetime
import pathlib
import sys
import threading
import time
from dataclasses import dataclass

import cv2
import keyboard

if sys.platform == 'win32':
    SCREENSHOTS_PATH = pathlib.Path('~/AppData/Roaming/.minecraft/screenshots')
elif sys.platform == 'darwin':
    SCREENSHOTS_PATH = pathlib.Path('~/Library/Application Support/minecraft/screenshots')
else:
    SCREENSHOTS_PATH = pathlib.Path('~/.minecraft/screenshots')


@dataclass
class Screenshot:
    path: pathlib.Path
    took_at: datetime.datetime
    iteration: int


def wait_for_keypress(event: threading.Event):
    """Waits for the end recording keypress."""

    time.sleep(0.5)  # to not stop the recording immediately
    keyboard.wait('ctrl+shift+f10')
    event.set()


def main(args: argparse.Namespace):
    print('Welcome to the Minecraft screenshot recorder.')
    print('To start and stop recording, press CTRL + SHIFT + F10.')
    print('After you are done recording, your screenshots will be processed into a video.')

    keyboard.wait('ctrl+shift+f10')

    print('Recording started...')

    done = threading.Event()
    threading.Thread(None, wait_for_keypress, args=(done,)).start()

    start_time = datetime.datetime.now()

    while not done.is_set():
        keyboard.press_and_release(args.keybind)
        time.sleep(0.1)

    end_time = datetime.datetime.now()
    print('Recording stopped.')

    print('Processing screenshots...')
    screenshots: list[Screenshot] = []

    for screenshot in args.directory.iterdir():
        name = screenshot.name.split('_')

        # parse the time the screenshot was taken.
        # I'm sure there's a better way to do this, but whatever.

        if len(name) == 3:
            date, time_, iteration = name
            iteration = int(iteration.split('.')[0])
        elif len(name) == 2:
            date, time_ = name
            iteration = 0
        else:
            continue

        split_date = date.split('-')
        if len(split_date) != 3:
            # some minecraft mods take higher quality screenshots, which we want to avoid
            continue

        year, month, day = split_date
        hour, minute, second = time_.split('.')[:3]
        screenshot_time = datetime.datetime(
            int(year), int(month), int(day), int(hour), int(minute), int(second)
        )

        # for sorting
        screenshot_time = screenshot_time.replace(microsecond=iteration)

        if start_time <= screenshot_time <= end_time:
            screenshots.append(Screenshot(screenshot, screenshot_time, iteration))

    if not screenshots:
        print('No screenshots taken. Aborting...')
        return

    screenshots = sorted(screenshots, key=lambda s: s.took_at)

    # calculate FPS
    counter = collections.Counter([s.took_at.replace(microsecond=0) for s in screenshots])
    average_fps = counter.total() // len(counter.keys())

    print('Generating video...')

    frames = []

    for screenshot in screenshots:
        frame = cv2.imread(str(screenshot.path.resolve()))  # type: ignore
        frames.append(frame)

    height, width, layers = frames[0].shape
    size = (width, height)

    writer = cv2.VideoWriter(  # type: ignore
        args.output, cv2.VideoWriter_fourcc(*'DIVX'), average_fps, size  # type: ignore
    )

    for frame in frames:
        writer.write(frame)

    writer.release()

    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Minecraft screenshot video recorder')
    parser.add_argument(
        '-d',
        '--directory',
        help='The screenshot directory (will try to find if not provided)',
        type=pathlib.Path,
        default=SCREENSHOTS_PATH,
    )
    parser.add_argument(
        '-o',
        '--output',
        help='The output file (should be an AVI file)',
        default='output.avi',
    )
    parser.add_argument(
        '--keybind',
        help='The Minecraft screenshot keybind (defaults to f2)',
        default='f2',
    )

    args = parser.parse_args()
    main(args)
