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

from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class LabelRule:
    name: str
    state: Literal["present", "absent", "update"]
    title: str
    description: Optional[str] = None
    color: Optional[str] = None
    new_title: Optional[str] = None
    new_color: Optional[str] = None
    new_description: Optional[str] = None

    def __post_init__(self):
        if self.state == "present":
            if not self.description or not self.color:
                raise ValueError(
                    "For 'present' state, description and color are required."
                )
        elif self.state == "update":
            if not any([self.new_title, self.new_color, self.new_description]):
                raise ValueError(
                    "For 'update' state, at least one of new_title, new_color, or new_description must be provided."
                )
        elif self.state == "absent":
            if any(
                [
                    self.description,
                    self.color,
                    self.new_title,
                    self.new_color,
                    self.new_description,
                ]
            ):
                raise ValueError(
                    "For 'absent' state, only name and title should be provided."
                )

    def to_dict(self):
        result = {
            "name": self.name,
            "label": {"state": self.state, "title": self.title},
        }

        if self.state == "present":
            result["label"]["description"] = self.description
            result["label"]["color"] = self.color
        elif self.state == "update":
            if self.new_title:
                result["label"]["new_title"] = self.new_title
            if self.new_color:
                result["label"]["new_color"] = self.new_color
            if self.new_description:
                result["label"]["new_description"] = self.new_description

        return result
