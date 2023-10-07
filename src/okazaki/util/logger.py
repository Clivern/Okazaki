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

import logging


class Logger:
    """
    The Logger class provides a centralized way to manage and retrieve logger instances.

    Attributes:
        loggers (dict): A class-level dictionary to store logger instances, keyed by name.
    """

    loggers = {}

    def get_logger(self, name=__name__):
        """
        Retrieves or creates a logger instance for the given name.

        Args:
            name (str, optional): The name of the logger. Defaults to the name of the
                                  module where this method is called (__name__).

        Returns:
            logging.Logger: A logger instance corresponding to the given name.

        Example:
            >>> logger = Logger().get_logger()
            >>> logger.info("This is an info message")
        """
        if name in self.loggers:
            return self.loggers[name]

        self.loggers[name] = logging.getLogger(name)

        return self.loggers[name]
