# shotcraft

A Minecraft screenshot video recorder.  
This is just a dumb idea that I had (and actually acted upon).

## Example

The video shown here is a GIF so I can display it in the README.
The actual output of the program is an AVI file.

![example](./examples/example.gif)

## Installation

Python 3.10+, [Poetry](https://python-poetry.org/), and Git are required to install and run the recorder.

```sh
# Download the project

# MacOS/Linux
python3 -m pip install -U git+https://github.com/Fyssion/shotcraft.git

# Windows
py -3 -m pip install -U git+https://github.com/Fyssion/shotcraft.git

# Install the dependencies
poetry install
```

## Usage

shotcraft is a command-line program.
Simply run shotcraft by entering the following command in a terminal or command prompt.

> Note: On Linux, shotcraft must be root to run. This is a dependency limitation.

```sh
# MacOS
python3 shotcraft.py

# Linux
sudo /path/to/python shotcraft.py

# Windows
py -3 shotcraft.py
```

## Advanced Usage

```sh
$ python shotcraft.py --help
usage: shotcraft.py [-h] [-d DIRECTORY] [-o OUTPUT] [--keybind KEYBIND]

Minecraft screenshot video recorder

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The screenshot directory (will try to find if not provided)
  -o OUTPUT, --output OUTPUT
                        The output file (should be an AVI file)
  --keybind KEYBIND     The Minecraft screenshot keybind (defaults to f2)
```

## Contributing

If you find a bug, have a feature request, or want to contribute code,
feel free to open an issue or pull request.

## License

This project is licensed under the [MIT License](./LICENSE).
