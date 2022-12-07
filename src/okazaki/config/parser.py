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

import yaml
from .label_rule import LabelRule


class Parser:
    def __init__(self, yaml_file, values_attr = "data"):
        self._yaml_file = yaml_file
        self._config = self.load_yaml()
        self._values_attr = values_attr
        self._label_rules: List[LabelRule] = []

    def load_yaml(self):
        with open(self._yaml_file, 'r') as file:
            return yaml.safe_load(file)

    def pipeline_set_data_item(self):
        data = self._config.get(self._values_attr, {})

        def replace_data_references(obj):
            if isinstance(obj, dict):
                return {k: replace_data_references(v) for k, v in obj.items()}

            elif isinstance(obj, list):
                return [replace_data_references(item) for item in obj]

            elif isinstance(obj, str) and obj.startswith('${var.'):
                item_key = obj[6:-1]  # Remove '${var.' prefix and '}' suffix
                return data.get(item_key, obj)

            else:
                return obj

        self._config = replace_data_references(self._config)

    def extract_label_rules(self):
        rules = self._config.get('rules', [])

        for rule in rules:
            if 'label' in rule:
                label_rule = LabelRule(
                    name=rule['name'],
                    state=rule['label']['state'],
                    title=rule['label']['title'],
                    description=rule['label'].get('description'),
                    color=rule['label'].get('color'),
                    new_title=rule['label'].get('new_title'),
                    new_color=rule['label'].get('new_color'),
                    new_description=rule['label'].get('new_description')
                )

                self._label_rules.append(label_rule)

    def process_config(self):
        pipelines = [
            self.pipeline_set_data_item,
            self.extract_label_rules,
            # Add more pipeline methods here
        ]

        for pipeline in pipelines:
            pipeline()

    def get_processed_config(self):
        return self._config

    def print_processed_config(self):
        print(yaml.dump(self._config, default_flow_style=False))

    def get_label_rules(self):
        return self._label_rules
