# MIT License
#
# Copyright (c) 2022 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import yaml


class Config():
    """This class parses repository .hippo.yml file"""

    _result = {}
    _data = {}
    _rule = {}
    _bot = {}
    _workflow = {}

    def __init__(self, file_path):
        """Class constructor"""
        self._file_path = file_path

    @classmethod
    def from_file(cls, file_path):
        """Creates an instance from a file path"""
        return Config(file_path)

    @property
    def data(self):
        """Get data property"""
        return self._data

    @property
    def rule(self):
        """Get rule property"""
        return self._rule

    @property
    def bot(self):
        """Get bot property"""
        return self._bot

    @property
    def workflow(self):
        """Get workflow property"""
        return self._workflow

    def parse(self):
        """Parse the repo config file"""
        if not os.path.exists(self._file_path):
            raise FileNotFoundError("File {} not exists".format(self._file_path))

        self._result = yaml.safe_load(open(self._file_path))

        if "rule" in self._result.keys():
            self._rule = self._result["rule"]

        if "bot" in self._result.keys():
            self._bot = self._result["bot"]

        if "workflow" in self._result.keys():
            self._workflow = self._result["workflow"]

        if "data" in self._result.keys():
            for value in self._parse_item("", self._result["data"]):
                self._data[value[0]] = value[1]

    def _parse_item(self, parent="", sub_items={}):
        for key, value in sub_items.items():
            if isinstance(value, dict):
                yield from self._parse_item(key if parent == "" else "{}.{}".format(parent, key), value)
            else:
                yield (key, value) if parent == "" else ("{}.{}".format(parent, key), value)
