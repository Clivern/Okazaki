# MIT License
#
# Copyright (c) 2022 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
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


class FileSystem:
    """
    The FileSystem class provides utility methods for file operations.

    This class currently offers a method to read the contents of a file.
    """

    @classmethod
    def read_file(cls, file_path):
        """
        Reads the contents of a file.

        This method opens the specified file in read mode and returns its entire contents as a string.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The contents of the file as a string.
        """
        with open(file_path, "r") as f:
            return f.read()
