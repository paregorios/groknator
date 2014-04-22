#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
from bs4 import BeautifulSoup
from http import HTTPGrokrrr
from indexers.markup import ElementIndexer, AttributeIndexer, RDFaIndexer, MetaIndexer
import logging
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
        ai = AttributeIndexer(ei)
        self.html['attributes'] = ai.index(soup)
        # index words
        # index meta tags
        mi = MetaIndexer()
        self.meta = mi.index(soup, self.http['urlgot'])
        # index schema.org microdata
        # open graph?
        # index rdfa microdata
        ri = RDFaIndexer(attribute_indexer=ai)
        self.rdfa = ri.index(soup)
        # identify alternate formats referenced in links
        # what is @rel attribute and how to capture?

