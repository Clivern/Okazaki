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

import yaml

from okazaki.util import Logger
from .label_rule import LabelRule
from .issue_rule import IssueRule
from .pull_request_rule import PullRequestRule
from typing import List


class ConfigParser:
    """
    A class for parsing and processing configuration data.
    """

    def __init__(self, config, values_attr="data", logger=None):
        """
        Initialize the ConfigParser.
        """
        self._config = config
        self._values_attr = values_attr
        self._label_rules: List[LabelRule] = []
        self._issue_rules: List[IssueRule] = []
        self._pull_request_rules: List[PullRequestRule] = []
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def _pipeline_set_data_item(self):
        """
        Process the configuration to replace data references.
        """
        data = self._config.get(self._values_attr, {})

        def replace_data_references(obj):
            if isinstance(obj, dict):
                return {k: replace_data_references(v) for k, v in obj.items()}

            elif isinstance(obj, list):
                return [replace_data_references(item) for item in obj]

            elif isinstance(obj, str) and obj.startswith("${var."):
                # Remove '${var.' prefix and '}' suffix
                item_key = obj[6:-1]
                return data.get(item_key, obj)

            else:
                return obj

        self._config = replace_data_references(self._config)

    def _extract_label_rules(self):
        """
        Extract label rules from the configuration.
        """
        rules = self._config.get("rules", [])

        for rule in rules:
            if "label" in rule:
                label_rule = LabelRule(
                    name=rule["name"],
                    state=rule["label"]["state"],
                    title=rule["label"]["title"],
                    description=rule["label"].get("description"),
                    color=rule["label"].get("color"),
                    new_title=rule["label"].get("new_title"),
                    new_color=rule["label"].get("new_color"),
                    new_description=rule["label"].get("new_description"),
                )

                self._label_rules.append(label_rule)

    def _extract_issue_rules(self):
        """
        Extract issue rules from the configuration.
        """
        pass

    def _extract_pull_request_rules(self):
        """
        Extract pull request rules from the configuration.
        """
        pass

    def process_config(self):
        """
        Process the configuration by running all pipeline methods.
        """
        pipelines = [
            self._pipeline_set_data_item,
            self._extract_label_rules,
            self._extract_issue_rules,
            self._extract_pull_request_rules,
            # Add more pipeline methods here
        ]

        for pipeline in pipelines:
            pipeline()

    def get_processed_config(self):
        """
        Get the processed configuration.
        """
        return self._config

    def print_processed_config(self):
        """
        Print the processed configuration in YAML format.
        """
        print(yaml.dump(self._config, default_flow_style=False))

    def get_label_rules(self):
        """
        Get the extracted label rules.
        """
        return self._label_rules

    def get_issue_rules(self):
        """
        Get the extracted issue rules.
        """
        return self._issue_rules

    def get_pull_request_rules(self):
        """
        Get the extracted pull request rules.
        """
        return self._pull_request_rules
