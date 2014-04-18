#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
from bs4 import BeautifulSoup
from http import HTTPGrokrrr
import logging
import re
import urllib2

HTMLMIMETYPES = [
    'text/html',
    'application/xhtml+xml'
]


DEFAULTHEADERS = {
    'User-Agent' : 'GroknatorHTMLGrokrrrbot/0.1 (+https://github.com/paregorios/groknator)',
    'Accept' : ','.join(HTMLMIMETYPES)
}

module_logger = logging.getLogger('groknator.grokrrrs.html')

class HTMLGrokrrr(BaseGrokrrr, HTTPGrokrrr):
    """
    A grokrrr class that knows how to work with HTML
    """

    def __init__(self):
        self.html = {}
        logger = logging.getLogger('groknator.grokrrrs.html.HTMLGrokrrr')
        try:
            self.loggers['html'] = logger
        except AttributeError:
            self.loggers = {}
            self.loggers['html'] = logger
        HTTPGrokrrr.__init__(self)
        BaseGrokrrr.__init__(self)

    def fetch(self, url, headers=DEFAULTHEADERS):
        HTTPGrokrrr.fetch(self, url, headers)

    def grok(self):
        logger = self.loggers['html']
        try:
            contenttype = self.http['response_headers']['content-type']
        except KeyError:
            logger.warning('response headers did not indicate a mimetype, so assuming text/html')
            mimetype = 'text/html'
        else:
            if ';' in contenttype:
                mimetype, charset = contenttype.split(';')
            else:
                mimetype = contenttype.strip()
        if mimetype in HTMLMIMETYPES:
            logger.debug('treating content as %s' % mimetype)
            soup = BeautifulSoup(self.rawcontent)
            self.html['soup'] = soup
        else:
            logger.error('content was not grokked because there is no handler for mimetype %s' % mimetype)
            return

        # index elements
        ei = ElementIndexer()
        self.html['elements'] = ei.index(soup)
        # index attributes
        # index words
        # index meta tags
        # index schema.org microdata
        # index rdfa microdata
        # identify alternate formats referenced in links
        # what is @rel attribute and how to capture?

class HTMLIndexer:
    """
    basic indexer class ClassName(object):
    """

    def __init__(self):
        pass

class ElementIndexer(HTMLIndexer):
    """
    foo
    """

    def __init__(self):
        self.logger = logging.getLogger('groknator.grokrrrs.html.ElementIndexer')
        HTMLIndexer.__init__(self)

    def index(self, soup):
        logger = self.logger
        elements = {}
        tagnames = set([t.name.strip() for t in soup.find_all(True)])
        for tagname in tagnames:
            elements[tagname] = {}
            tags = soup.find_all(tagname)
            elements[tagname]['count'] = len(tags)
            elements[tagname]['instances'] = []
            for tag in tags:
                ele = {}
                ele['attributes'] = []
                for a in sorted(tag.attrs.keys()):
                    val = tag.attrs[a]
                    if type(val) is list:
                        val = u' '.join(val)
                    p = re.compile(u'\s+')
                    val = p.sub(u' ', val).strip()
                    ele['attributes'].append({a:val})
                elements[tagname]['instances'].append(ele)
        logger.debug("elements: %s" % sorted(elements.keys()))
        return elements


