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


class Milestone:
    """
    The Milestone class provides methods to interact with GitHub milestones.

    Attributes:
        _app (App): An instance of the App class used to access the GitHub client.
    """

    def __init__(self, app):
        """
        Initializes the Milestone class with the given application instance.

        Args:
            app (App): An instance of the App class that provides access to the GitHub client.
        """
        self._app = app

    def create_milestone(self, repo, title, state='open', description=None, due_on=None):
        """
        Creates a new milestone in the specified repository.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").
            title (str): The title of the milestone.
            state (str, optional): The state of the milestone. Defaults to 'open'.
            description (str, optional): The description of the milestone. Defaults to None.
            due_on (datetime, optional): The due date of the milestone. Defaults to None.

        Returns:
            github.Milestone.Milestone: The newly created milestone object.
        """
        return self._get_repo(repo).create_milestone(
            title,
            state=state,
            description=description,
            due_on=due_on
        )

    def get_milestones(self, repo, state='open'):
        """
        Retrieves milestones from the specified repository.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").
            state (str, optional): The state of the milestones to retrieve. Defaults to 'open'.

        Returns:
            github.PaginatedList.PaginatedList: A paginated list of milestone objects.
        """
        return self._get_repo(repo).get_milestones(
            state=state
        )

    def _get_repo(self, repo):
        """
        Helper method to get a repository object from the GitHub client.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").

        Returns:
            github.Repository.Repository: A GitHub repository object.
        """
        return self._app.get_client().get_repo(repo)
