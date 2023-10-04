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

from github import GithubObject
from okazaki.exception import NotFound


class Issue:

    def __init__(self, app):
        self._app = app

    def get_issue(self, repo, number):
        try:
            return self._get_repo(repo).get_issue(
                number=number
            )
        except Exception:
            return None

    def create_issue(
        self,
        repo,
        title,
        body,
        assignees=GithubObject.NotSet,
        labels=GithubObject.NotSet,
        milestone=GithubObject.NotSet
    ):

        return self._get_repo(repo).create_issue(
            title=title,
            body=body,
            assignees=assignees,
            labels=labels,
            milestone=milestone
        )

    def get_labels(self, repo, labels=[]):

        result = []

        for label in labels:
            result.append(self._get_repo(repo).get_label(label))

        return result if len(result) > 0 else None

    def close_issue(self, repo, number):

        issue = self.get_issue(repo, number)

        if issue is not None:
            issue.edit(state='closed')
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def reopen_issue(self, repo, number):

        issue = self.get_issue(repo, number)

        if issue is not None:
            issue.edit(state='open')
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def edit_issue(
        self,
        repo,
        number,
        title,
        body,
        assignees=GithubObject.NotSet,
        labels=GithubObject.NotSet,
        milestone=GithubObject.NotSet,
        state=GithubObject.NotSet
    ):
        issue = self.get_issue(repo, number)

        if issue is not None:
            issue.edit(
                title=title,
                body=body,
                assignees=assignees,
                labels=labels,
                milestone=milestone,
                state=state
            )
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def add_comment(self, repo, number, body):

        issue = self.get_issue(repo, number)

        if issue is not None:
            return issue.create_comment(body)
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def get_comments(self, repo, number):

        issue = self.get_issue(repo, number)

        if issue is not None:
            return issue.get_comments()
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def add_labels(self, repo, number, labels):

        issue = self.get_issue(repo, number)

        if issue is not None:
            return issue.add_to_labels(*labels)
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def remove_label(self, repo, number, label):

        issue = self.get_issue(repo, number)

        if issue is not None:
            return issue.remove_from_labels(label)
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def get_events(self, repo, number):

        issue = self.get_issue(repo, number)

        if issue is not None:
            return issue.get_events()
        else:
            raise NotFound(f"Repository '{repo}' Issue with number '{number}' not found")

    def create_milestone(self, repo, title, state='open', description=None, due_on=None):

        return self._get_repo(repo).create_milestone(
            title,
            state=state,
            description=description,
            due_on=due_on
        )

    def get_milestones(self, repo, state='open'):

        return self._get_repo(repo).get_milestones(
            state=state
        )

    def search_issues(self, query):

        return self._app.get_client().search_issues(query)

    def _get_repo(self, repo):

        return self._app.get_client().get_repo(repo)
