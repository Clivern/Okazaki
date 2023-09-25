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

import jwt
import json
import time
import calendar
import datetime
import requests
import logging
from dateutil import parser
from http import HTTPStatus
from tent.exception.github_api_error import GithubApiError


class App():
    """Github App Class"""

    def __init__(self, api_url="https://api.github.com"):
        """
        Class Constructor

        Args:
            api_url: the github API URL
        """
        self._api_url = api_url
        self._logger = logging.getLogger(__name__)

    def is_token_expired(self, expire_at, drift_in_minutes=10):
        """
        Check if token expired or not

        Args:
            expire_at: the token expire date
            drift_in_minutes: a drift in minutes

        Returns:
            Whether the token expired or not
        """
        expire_at_dt = parser.isoparse(expire_at)
        now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=drift_in_minutes)

        return now > expire_at_dt

    def fetch_access_token(self, secret_key, app_id, installation_id):
        """
        Fetch Access Token with installation ID

        Access token is valid for one hour

        Args:
            secret_key: The secret key
            app_id: the application ID
            installation_id: the installation ID

        Returns:
            The access token data
        """
        headers = {
            "Authorization": "Bearer {}".format(self._get_jwt_token(secret_key, app_id)),
            "Accept": 'application/vnd.github.v3+json'
        }

        url = "{}/app/installations/{}/access_tokens".format(self._api_url, installation_id)

        try:
            request = requests.post(
                url,
                headers=headers,
                data=''
            )

            if self._is_success(request.status_code):
                self._logger.debug("Github request to {} succeeded: {} {}".format(
                    url,
                    request.status_code,
                    request.text
                ))

                return self._to_obj(request.text)

            msg = "Error, while calling github api {}, response: {}".format(url, request.text)
        except Exception:
            msg = "Error, while calling github api {}, response: {}".format(url, request.text)

        self._logger.error(msg)

        raise GithubApiError(msg)

    def _get_jwt_token(self, secret_key, app_id):
        """
        Get JWT token

        Args:
            secret_key: the secret key
            app_id: The application ID

        Returns:
            The JWT token
        """
        return jwt.encode({
            'iat': calendar.timegm(time.gmtime()) - 60,
            'exp': calendar.timegm(time.gmtime()) + 600,
            'iss': app_id
        }, secret_key, algorithm='RS256')

    def _is_success(self, http_code):
        """
        Check if request succeeded

        Args:
            http_code: the HTTP code

        Returns:
            Whether the HTTP request succeeded or not
        """
        return http_code >= HTTPStatus.OK and http_code < HTTPStatus.MULTIPLE_CHOICES

    def _to_obj(self, json_text):
        """
        Convert JSON to Object

        Args:
            json_text: the JSON response

        Returns:
            An Object
        """
        return json.loads(json_text)

    def _to_json(self, obj):
        """
        Convert Object into JSON

        Args:
            obj: an object

        Returns:
            Object as JSON
        """
        return json.dumps(obj)
