"""This module provides RP Tree main module"""

import os
import pathlib
import sys

PIPE = "|"
ELBOW = "|___" # used if entry is last in the directory
TEE = "|---" # used if entry is NOT last in directory
PIPE_PREFIX = "| "
SPACE_PREFIX = " "

class DirectoryTree:
    """Represents a directory tree"""
    def __init__(self, root_dir, output_file = sys.stdout):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir) # uses OOP "composition" technique to define a "has a" relationship

    def generate(self):
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            # wrap the tree in a markdown code block
            tree.insert(0, "```") # could be better optimized via .appendleft() for bigger directories
            tree.append("```")
            self._output_file = open(
                self._output_file, mode = "w", encoding = "UTF-8"
            )
            with self._output_file as stream: # with statement ensures resources are properly released even if errors occur (e.g. closing files)
                for entry in tree:
                    print(entry, file = stream)

class _TreeGenerator:
    def __init__(self, root_dir): # holds tree's root directory path
        self._root_dir = pathlib.Path(root_dir)
        self._tree = [] # list containing all the entries that shape the tree diagram

    def build_tree(self): # generates and returns the directory tree diagram
        self._tree_head() #used to build head
        self._tree_body(self._root_dir)  # generate rest of diagram
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}") # adds name of the root directory to ._tree
        self._tree.append(PIPE) # connects root directory to rest of tree

    def _tree_body(self, directory, prefix = ""):
        entries = directory.iterdir() #.iterdir() returns an iterator over files and subdirectories contained in directory
        entries = sorted(entries, key = lambda entry:entry.is_file()) # lambda func checks if the entry is a file and returns either True or False
        entries_count = len(entries)
        for index, entry in enumerate(entries): # enumerate() associates an index to each entry
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(directory = directory, prefix = prefix) #indirect recursive call
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector}{file.name}")