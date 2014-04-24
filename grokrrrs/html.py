#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
from bs4 import BeautifulSoup
from file import TextFileGrokrrr
from http import HTTPGrokrrr
from indexers.markup import ElementIndexer, AttributeIndexer, RDFaIndexer, MetaIndexer
import logging
import os
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

IGNORETAGSFORTEXT = [
    'script'
]

module_logger = logging.getLogger('groknator.grokrrrs.html')

class HTMLGrokrrr(BaseGrokrrr, HTTPGrokrrr, TextFileGrokrrr):
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
        try:
            http = self.http
        except AttributeError:
            HTTPGrokrrr.__init__(self)
        try:
            textfile = self.file
        except AttributeError:
            TextFileGrokrrr.__init__(self)
        try:
            base = self.base
        except AttributeError:
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
            puretext = u''
            for t in soup.html.body.contents:
                logger.debug("t.name: %s" % t.name)
                if t.name not in IGNORETAGSFORTEXT:
                    try:
                        puretext = u' '.join((puretext, t.get_text("|", strip=True)))
                    except AttributeError:
                        puretext = u' '.join((puretext, unicode(t)))
            p = re.compile(u'\s+')
            puretext = p.sub(u' ', puretext).strip()
            logger.debug("puretext: '%s'" % puretext)
            self.puretext = puretext
        else:
            logger.error('content was not grokked because there is no handler for mimetype %s' % mimetype)
            return

        # index elements
        ei = ElementIndexer()
        self.html['elements'] = ei.index(soup)
        # index attributes
        ai = AttributeIndexer(ei)
        self.html['attributes'] = ai.index(soup)
        # index meta tags
        mi = MetaIndexer()
        self.meta = mi.index(soup, self.documenturl)
        # index rdfa microdata
        ri = RDFaIndexer(attribute_indexer=ai)
        self.rdfa = ri.index(soup)
        # identify alternate formats referenced in links
        # what is @rel attribute and how to capture?
        # index words
        # index schema.org microdata
        # open graph?
        # languages
        # scripts
        # encodings (http, meta, bs4-sniffed)
        # word frequency
        # plantext regex matches
        # colon postfixed terms (isbn issn, urn, doi)
        # emails
        # cool ancient uris

class SoupSpider():
    """ 
    helper class for working with BeautifulSoup soups
    """

    def __init__(self):
        pass

    def walk(self, soup, targets=['textnodes',]):
        """
        recursively walk the soup tree in document order, building a list of values as dictated
        by the 'targets' attribute. Eventually, would like to support the following target 
        values, probably putting results for each node in a dictionary in the list: nodes, 
        textnodes, elements, elementnames, attributes, attributenames
        """
        pass

