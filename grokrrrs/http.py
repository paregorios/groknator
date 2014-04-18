#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
import logging
import urllib2

module_logger = logging.getLogger('groknator.grokrrrs.http')

DEFAULTHEADERS = {
    'User-Agent' : 'GroknatorHTTPGrokrrrbot/0.1 (+https://github.com/paregorios/groknator)',
}


class HTTPGrokrrr(BaseGrokrrr):
    """
    A grokrrr class that knows how to request things via HTTP
    """

    def __init__(self):
        self.http = {}
        logger = logging.getLogger('groknator.grokrrrs.base.HTTPGrokrrr')
        try:
            self.loggers['http'] = logger
        except AttributeError:
            self.loggers = {}
            self.loggers['http'] = logger
        BaseGrokrrr.__init__(self)

    def fetch(self, url, headers=DEFAULTHEADERS):
        """
        retrieve content over the web via http
        """
        logger = self.loggers['http']
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            logger.error("failed to retrieve the resource at %s" % url)
            raise
        urlgot = response.geturl()
        rawcontent = response.read()
        if urlgot != url:
            logger.info("successfully retrieved resource from %s, redirected from %s" % (urlgot, url))
            self.http['redirect'] = True
        else:
            logger.info("successfully retrieved resource from %s" % url)
            self.http['redirect'] = False
        rheaders = response.info()
        
        # store useful info on the object for later access
        self.http['request'] = {}
        self.http['request']['headers'] = headers
        self.http['urlsought'] = url
        self.http['urlgot'] = urlgot
        self.http['response'] = response
        self.http['response_headers'] = {}
        for k in sorted(rheaders.keys()):            
            logger.debug("response header %s: '%s'" % (k, rheaders[k]))
            self.http['response_headers'][k.strip().lower()] = rheaders[k].strip()        
        self.rawcontent = rawcontent
