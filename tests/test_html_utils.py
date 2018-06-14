# -*- coding: utf-8 -*-
import pytest
from html_utils import strip_html_tags


@pytest.mark.parametrize(('before', 'after', 'rules'), [
    ('<h1>header1</h1>', 'header1', ['h1']),
    ('<script">alert(233)</script>', '', ['script.+'])
])
def test_strip_html_tags(before, after, rules):
    assert strip_html_tags(before, rules) == after
