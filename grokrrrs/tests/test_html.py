#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equal

from grokrrrs.html import HTMLGrokrrr

import os


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
        # html.fetch() doesn't do anything other than invoke http.fetch() so see tests for http

def test_html_get():
    g = HTMLGrokrrr()
    if g is not None:
        here = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(here, 'data', 'lorem-ipsum-utf8.html')
        g.get(filepath)
        # html.fetch() doesn't do anything other than invoke textfile.fetch() so see tests for file

def test_html_grok():
    g = HTMLGrokrrr()
    if g is not None:
        here = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(here, 'data', 'lorem-ipsum-utf8.html')
        g.get(filepath)
        g.grok()
        h = g.html
        # Beautiful Soup gets invoked on the content, and the result stored on the object
        assert_equals('soup' in h.keys(), True)
        # store just text nodes as pure text
        assert_equals('puretext' in dir(g), True)
        assert_equals(g.puretext, u'Maecenas convallis mauris nec accumsan malesuada. Morbi enim lorem, porttitor sed tellus vel, semper lobortis sapien. Donec dapibus neque mi, a aliquam nibh vehicula vel. Ηας κυις ελιγενδι δισεντιας νο. Λεγερε κυαεστιο ιδ μελ, ει λεγερε ηωνεσθαθις φιξ. Φιμ λωρεμ λεγιμυς αδ, εξ φερο φενιαμ σομμοδο υσυ. Ει φιξ δολωρυμ. كلا أدولف ديسمبر الوزراء أي, ثمّة واستمر حين أي. عن يبق سلاح وبدون الصعداء. أراض الفاشي الجنوبي مدن لم, و بال بداية بلديهما. كلا جدول. 化読入会芸田側測辞藤評支空指。済真院賀水前祐伸文録愛革活。転問郎輪雨鹿条社訴民多持物力語放。以木蔵写補鈴捨態暮裁号閉博針買真責味多。組質権登調北文土州首演鑑計果訴職情表投明。必攻収月選平碁鮮問内政弁技表授部引止作梨。式見惑末業属年葉経掲属大東。王暮意負歳類間容女芸京出天馬止転。日専東籍短性鈴職暮止基重次文界。')
        # There should be indexes on the object of all elements and all attributes in the soup
        assert_equals('elements' in h.keys(), True)
        assert_equals(sorted(h['elements'].keys()), ['body', 'head', 'html', 'p', 'title'])
        assert_equals('attributes' in h.keys(), True)
        assert_equals(sorted(h['attributes'].keys()), ['xmlns',])
        # There should also be indexes on the object of all meta elements and all detected rdfa
        assert_equals('meta' in dir(g), True)
        assert_equals('rdfa' in dir(g), True)
