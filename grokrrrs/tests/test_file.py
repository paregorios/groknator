#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equal

from grokrrrs.file import TextFileGrokrrr

import os


def test_textfile_creation():
    g = TextFileGrokrrr()
    assert_equals(g.__class__.__name__, 'TextFileGrokrrr')

def test_textfile_properties():
    g = TextFileGrokrrr()
    if g is not None:
        assert_equals(type(g.file), dict)
        assert_equals(g.loggers['file'].__class__.__name__, 'Logger')

def test_textfile_methods():
    g = TextFileGrokrrr()
    if g is not None:
        assert_equals('get' in dir(g), True)

def test_textfile_get():
    g = TextFileGrokrrr()
    if g is not None:
        here = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(here, 'data', 'lorem-ipsum-utf8.html')
        g.get(filepath)
        f = g.file
        # fetch stashes the raw content as well
        assert_equals('rawcontent' in dir(g), True)
        assert_equals(type(g.rawcontent), unicode) # compare http.fetch(), which stores rawcontent as str



