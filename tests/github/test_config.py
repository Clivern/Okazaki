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

import os
import pytest

from okazaki.github.config import Config


def test_config():
    dt = Config.from_file("{}/specs/.test_case_1.yml".format(os.getcwd()))
    dt.parse()

    assert dt.data["a.b.c.d"] == 'hi'
    assert dt.data["a.b.e.f"] == 'there'
    assert dt.data["a.b.e.k"] == ['a', 'b', 'c']
    assert dt.data["k.u.p"] == True
    assert dt.rule[0]['name'] == "create kind/issue label"
    assert dt.bot['acl']['groups'][0]['name'] == 'lead'
    assert dt.workflow['first_contribution']['active_for'][0] == 'prs'

def test_data_error():
    with pytest.raises(FileNotFoundError):
        dt = Config.from_file("{}/specs/.test_case_2.yml".format(os.getcwd()))
        dt.parse()
