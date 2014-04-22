#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from grokrrrs.base import BaseGrokrrr


def test_base_creation():
    b = BaseGrokrrr()
    assert_equals(b.__class__.__name__, 'BaseGrokrrr')

def test_base_properties():
    b = BaseGrokrrr()
    if b is not None:
        assert_equals(b.base, True)
        assert_equals(b.loggers['base'].__class__.__name__, 'Logger')

