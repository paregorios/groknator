#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equal

from grokrrrs.http import HTTPGrokrrr, DEFAULTHEADERS


def test_http_creation():
    g = HTTPGrokrrr()
    assert_equals(g.__class__.__name__, 'HTTPGrokrrr')

def test_http_properties():
    g = HTTPGrokrrr()
    if g is not None:
        assert_equals(type(g.http), dict)
        assert_equals(g.loggers['http'].__class__.__name__, 'Logger')

def test_http_methods():
    g = HTTPGrokrrr()
    if g is not None:
        assert_equals('fetch' in dir(g), True)

def test_http_fetch():
    g = HTTPGrokrrr()
    if g is not None:
        url = 'http://isaw.nyu.edu'
        g.fetch(url)
        h = g.http
        # if a redirect occurs, fetch will set a flag and report both the url requested and the url to which directed
        assert_equals('redirect' in h.keys(), True)
        assert_equals('urlsought' in h.keys(), True)
        assert_equals('urlgot' in h.keys(), True)
        assert_equals(h['redirect'], False)
        assert_equals(h['urlsought'], url)
        assert_equals(h['urlsought'], h['urlgot'])
        # fetch records both the request information and the response information, including all headers
        assert_equals('request' in h.keys(), True)
        assert_equals('headers' in h['request'].keys(), True)
        assert_equals('User-Agent' in h['request']['headers'].keys(), True)
        assert_equals(DEFAULTHEADERS['User-Agent'], h['request']['headers']['User-Agent'])
        assert_equals('response_headers' in h.keys(), True)
        assert_equals('content-type' in h['response_headers'].keys(), True)
        assert_equals('text/html;charset=utf-8', h['response_headers']['content-type'])
        # fetch stashes the raw content as well
        assert_equals('rawcontent' in dir(g), True)
        assert_equals(type(g.rawcontent), str) # compare text.fetch(), which stores rawcontent as unicode
        assert_equals('documenturl' in dir(g), True)



