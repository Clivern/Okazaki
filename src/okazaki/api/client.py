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

import json
import calendar
import time
import datetime
import jwt
import requests
from dateutil import parser
from http import HTTPStatus
from okazaki.util import Logger
from okazaki.util import FileSystem
from okazaki.exception import ApiError


class Client():

    def __init__(self, file_system=None, logger=None, github_api="https://api.github.com"):
        self.github_api = github_api
        self.logger = Logger().get_logger(__name__) if logger is None else logger
        self.file_system = FileSystem() if file_system is None else file_system

    def fetch_access_token(self, private_key_path, app_id, installation_id):
        return self._post(
            self._get_url("/app/installations/{}/access_tokens".format(installation_id)),
            self._get_headers(self._get_jwt_token(private_key_path, app_id)),
        )

    def is_token_expired(self, expire_at, drift_in_minutes=10):
        expire_at_dt = parser.isoparse(expire_at)

        now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            minutes=drift_in_minutes
        )

        return now > expire_at_dt

    def _get(self, url, headers={}):
        """Get Request"""
        try:
            self.logger.info("Perform a GET request to {}".format(url))

            request = requests.get(url, headers=headers)

            if self._is_success(request.status_code):
                self.logger.info("GET request to {} succeeded".format(url))

                return self._to_obj(request.text)
            else:
                msg = "Error, while calling github api {}, response: {}".format(url, request.text)

                self.logger.error(msg)

                raise ApiError(msg)
        except Exception:
            msg = "Error, while calling github api {}, response: {}".format(url, request.text)

            self.logger.error(msg)

            raise ApiError(msg)

    def _post(self, url, headers={}, data=""):
        """Post Request"""
        try:
            self.logger.info("Perform a POST request to {}".format(url))

            request = requests.post(url, headers=headers, data=data)

            if self._is_success(request.status_code):
                self.logger.info("POST request to {} succeeded".format(url))

                return self._to_obj(request.text)
            else:
                msg = "Error, while calling github api {}, response: {}".format(url, request.text)

                self.logger.error(msg)

                raise ApiError(msg)
        except Exception:
            msg = "Error, while calling github api {}, response: {}".format(url, request.text)

            self.logger.error(msg)

            raise ApiError(msg)

    def _put(self, url, headers={}, data=""):
        """Put Request"""
        try:
            self.logger.info("Perform a PUT request to {}".format(url))

            request = requests.put(url, headers=headers, data=data)

            if self._is_success(request.status_code):
                self.logger.info("PUT request to {} succeeded".format(url))

                return self._to_obj(request.text)
            else:
                msg = "Error, while calling github api {}, response: {}".format(url, request.text)

                self.logger.error(msg)

                raise ApiError(msg)
        except Exception:
            msg = "Error, while calling github api {}, response: {}".format(url, request.text)

            self.logger.error(msg)

            raise ApiError(msg)

    def _patch(self, url, headers={}, data=""):
        """Patch Request"""
        try:
            self.logger.info("Perform a PATCH request to {}".format(url))

            request = requests.patch(url, headers=headers, data=data)

            if self._is_success(request.status_code):
                self.logger.info("PATCH request to {} succeeded".format(url))

                return self._to_obj(request.text)
            else:
                msg = "Error, while calling github api {}, response: {}".format(url, request.text)

                self.logger.error(msg)

                raise ApiError(msg)
        except Exception:
            msg = "Error, while calling github api {}, response: {}".format(url, request.text)

            self.logger.error(msg)

            raise ApiError(msg)

    def _delete(self, url, headers={}):
        """Delete Request"""
        try:
            self.logger.info("Perform a DELETE request to {}".format(url))

            request = requests.delete(url, headers=headers)

            resp_time = (time.time() - start_time) * 1000

            if self._is_success(request.status_code):
                self.logger.info("DELETE request to {} succeeded".format(url))

                return self._to_obj("{}" if request.text == "" else request.text)
            else:
                msg = "Error, while calling github api {}, response: {}".format(url, request.text)

                self.logger.error(msg)

                raise ApiError(msg)
        except Exception:
            msg = "Error, while calling github api {}, response: {}".format(url, request.text)

            self.logger.error(msg)

            raise ApiError(msg)

    def _is_success(self, http_code):
        """Check if request succeeded"""
        return http_code >= HTTPStatus.OK and http_code < HTTPStatus.MULTIPLE_CHOICES

    def _to_obj(self, json_text):
        """Convert JSON to Object"""
        return json.loads(json_text)

    def _to_json(self, obj):
        """Convert Object into JSON"""
        return json.dumps(obj)

    def _get_url(self, rel_url):
        """Get Github API URL"""
        return "{}{}".format(self.github_api, rel_url)

    def _get_headers(self, token):
        """Get Headers"""
        return {
            "Authorization": "Bearer {}".format(token),
            "Accept": "application/vnd.github.v3+json",
        }

    def _get_jwt_token(self, private_key_path, app_id):
        """Get JWT token"""
        secret_key = self.file_system.read_file(private_key_path)

        return jwt.encode(
            {
                "iat": calendar.timegm(time.gmtime()) - 60,
                "exp": calendar.timegm(time.gmtime()) + 600,
                "iss": app_id,
            },
            secret_key,
            algorithm="RS256",
        )