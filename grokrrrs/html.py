#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
from http import HTTPGrokrrr
import logging
import urllib2

DEFAULTHEADERS = {
    'User-Agent' : 'GroknatorHTMLGrokrrrbot/0.1 (+https://github.com/paregorios/groknator)',
    'Accept' : 'text/html,application/xhtml+xml'
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
        pass

