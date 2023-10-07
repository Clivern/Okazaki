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


class PullRequest:
    """
    The PullRequest class provides methods to interact with GitHub repositories,
    specifically for operations related to branches and pull requests.

    Attributes:
        _app (App): An instance of the App class used to access the GitHub client.
    """

    def __init__(self, app):
        """
        Initializes the PullRequest class with the given application instance.

        Args:
            app (App): An instance of the App class that provides access to the GitHub client.
        """
        self._app = app

    def get_default_branch(self, repo):
        """
        Retrieves the default branch of a specified repository.

        Args:
            repo (str): The full name of the repository (e.g., "owner/repo").

        Returns:
            str: The name of the default branch.
        """
        return self._get_repo(repo).default_branch

    def create_branch(self, repo, source_branch, new_branch):
        """
        Creates a new branch in the specified repository.

        Args:
            repo (str): The full name of the repository.
            source_branch (str): The name of the branch to base the new branch on.
            new_branch (str): The name of the new branch to create.

        Returns:
            github.GitRef.GitRef: The newly created Git reference.
        """
        source_obj = self._get_repo(repo).get_branch(source_branch)
        return self._get_repo(repo).create_git_ref(
            ref=f'refs/heads/{new_branch}',
            sha=source_obj.commit.sha
        )

    def delete_branch(self, repo, branch_name):
        """
        Deletes a branch in the specified repository.

        Args:
            repo (str): The full name of the repository.
            branch_name (str): The name of the branch to delete.
        """
        ref = self._get_repo(repo).get_git_ref(f"heads/{branch_name}")
        ref.delete()

    def create_commit(self, repo, branch, file_path, file_content, commit_message):
        """
        Creates a new commit in the specified repository and branch.

        Args:
            repo (str): The full name of the repository.
            branch (str): The name of the branch to commit to.
            file_path (str): The path of the file to commit.
            file_content (str): The content of the file.
            commit_message (str): The commit message.

        Returns:
            github.ContentFile.ContentFile: The newly created content file.
        """
        return self._get_repo(repo).create_file(
            path=file_path,
            message=commit_message,
            content=file_content,
            branch=branch
        )

    def open_pr(self, repo, title, body, base_branch, head_branch):
        """
        Opens a new pull request in the specified repository.

        Args:
            repo (str): The full name of the repository.
            title (str): The title of the pull request.
            body (str): The body/description of the pull request.
            base_branch (str): The name of the branch to merge into.
            head_branch (str): The name of the branch containing the changes.

        Returns:
            github.PullRequest.PullRequest: The newly created pull request.
        """
        return self._get_repo(repo).create_pull(
            title=title,
            body=body,
            head=head_branch,
            base=base_branch
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
