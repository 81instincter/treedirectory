"""This module provides the RP Tree CLI"""
# cli.py

import argparse
import pathlib
import sys
from .import __version__ # imports version file in project
from rptree.rptree import DirectoryTree

def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print("The specified root directory does not exist.")
        sys.exit()
    tree = DirectoryTree(root_dir, output_file = args.output_file) # creates directory tree object
    tree.generate() # displays tree object

def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser( # instantiates method
        prog = "tree",
        description = "RP Tree, a directory tree generator",
        epilog = "Thanks for using RP Tree!",
    )
    parser.version = f"RP Tree v{__version__}"
    parser.add_argument("-v", "--version", action="version") # adds first optional argument to application's CLI
    parser.add_argument( # adds a second argument to the CLI
        "root_dir",
        metavar = "ROOT_DIR", # holds name of the argument in usage messages
        nargs = "?", # define number of values program can take under the argument at hand
        default = ".", # provides default value for argument at hand
        help = "Generate a full directory tree stating at ROOT_DIR", # describes what argument does
    )
    parser.add_argument(
        "-o",
        "--output_file",
        metavar = "OUTPUT_FILE",
        nargs = "?",
        default = sys.stdout,
        help = "Generate a full directory tree and save it to a file",
    )
    return parser.parse_args() # returns a namespace object with the supplied arguments

"""
Notes:

argparse.ArgumentParser() provides application's command name (prog), a short
description of the program, and an epilog phrase to display after user runs the
application's help option.


"""