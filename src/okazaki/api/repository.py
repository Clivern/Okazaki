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


class Repository:
    """
    The Repository class provides methods to interact with GitHub repositories.

    Attributes:
        _app (App): An instance of the App class used to access the GitHub client.
    """

    def __init__(self, app):
        """
        Initializes the Repository class with the given application instance.

        Args:
            app (App): An instance of the App class that provides access to the GitHub client.
        """
        self._app = app

    def get_contents(self, repo, file_path):
        """
        Retrieves the contents of a file from a specified repository.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").
            file_path (str): The path to the file within the repository.

        Returns:
            str: The decoded content of the file as a string.
            None: If the file is not found or an error occurs.

        Note:
            This method catches any exceptions that occur during the retrieval process
            and returns None in case of an error.
        """
        try:
            content = self._get_repo(repo).get_contents(file_path)
        except Exception as e:
            return None
        return content.decoded_content.decode()

    def _get_repo(self, repo):
        """
        Helper method to get a repository object from the GitHub client.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").

        Returns:
            github.Repository.Repository: A GitHub repository object.

        Note:
            This method uses the GitHub client provided by the App instance.
        """
        return self._app.get_client().get_repo(repo)
