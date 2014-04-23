#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equal

from grokrrrs.html import HTMLGrokrrr


def test_html_creation():
    g = HTMLGrokrrr()
    assert_equals(g.__class__.__name__, 'HTMLGrokrrr')

def test_html_properties():
    g = HTMLGrokrrr()
    if g is not None:
        assert_equals(type(g.html), dict)
        assert_equals(g.loggers['html'].__class__.__name__, 'Logger')

def test_html_methods():
    g = HTMLGrokrrr()
    if g is not None:
        assert_equals('fetch' in dir(g), True)
        assert_equals('grok' in dir(g), True)

def test_html_fetch():
    g = HTMLGrokrrr()
    if g is not None:
        url = 'http://isaw.nyu.edu'
        g.fetch(url)
        g.grok()
        h = g.html
        # Beautiful Soup gets invoked on the content, and the result stored on the object
        assert_equals('soup' in h.keys(), True)
        # There should be indexes on the object of all elements and all attributes in the soup
        assert_equals('elements' in h.keys(), True)
        assert_equals('attributes' in h.keys(), True)
        # There should also be indexes on the object of all meta elements and all detected rdfa
        assert_equals('meta' in dir(g), True)
        assert_equals('rdfa' in dir(g), True)



