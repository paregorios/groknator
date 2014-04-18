#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
from http import HTTPGrokrrr
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
            mimetype = self.http['response_headers']['content-type']
        except KeyError:
            logger.warning('response headers did not indicate a mimetype, so assuming text/html')
            mimetype = 'text/html'
        if mimetype in HTMLMIMETYPES:
            logger.debug('treating content as %s' % mimetype)
            soup = BeautifulSoup(self.content)
        else:
            logger.error('content was not grokked because there is no handler for mimetype %s' % mimetype)
            return

        # index elements
        # index attributes
        # index words
        # index meta tags
        # index schema.org microdata
        # index rdfa microdata
        # identify alternate formats referenced in links


