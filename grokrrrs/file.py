#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseGrokrrr
import chardet
import codecs
import logging
import os

module_logger = logging.getLogger('groknator.grokrrrs.file')

class TextFileGrokrrr(BaseGrokrrr):
    """
    a grokrrr class that knows how to work with text files
    """

    def __init__(self):
        self.file = {}
        logger = logging.getLogger('groknator.grokrrrs.html.FileGrokrrr')
        try:
            self.loggers['file'] = logger
        except AttributeError:
            self.loggers = {}
            self.loggers['file'] = logger
        try:
            base = self.base
        except AttributeError:
            BaseGrokrrr.__init__(self)

    def get(self, filepath, encoding=None):
        """
        get the contents of the requested file
        """

        logger = self.loggers['file']

        # normalize and absolutize path
        infn = os.path.abspath(filepath)
        if infn != filepath:
            logger.warning("filepath '%s' given to '%s'.get() is not an absolute path; using '%s'" % (filepath, self.__class__.__name__, infn))
        self.file['pathsought'] = filepath
        self.file['pathgot'] = infn

        # make sure we're dealing with a file and not something else
        if not os.path.isfile(infn):
            msg = "'%s' does not point to a valid file in %s" % (infn, self.__class__.__name__)
            logger.error(msg)
            raise IOError(msg)

        # try to figure out the encoding of the file
        bytes = min(32, os.path.getsize(infn))
        raw = open(infn, 'rb').read(bytes)
        if raw.startswith(codecs.BOM_UTF8):
            sysencoding = 'utf-8-sig'
        else:
            result = chardet.detect(raw)
            sysencoding = result['encoding']
        logger.debug("detected encoding: %s" % sysencoding)
        self.file['encoding'] = sysencoding
        if encoding is not None:
            logger.debug("specified encoding: %s" % encoding)
            if sysencoding != encoding:
                logger.warning("a file encoding was specified (%s) for %s, but %s detected a different encoding: %s; using %s" % (encoding, infn, self.__class__.__name__, sysencoding, encoding))
                self.file['encoding'] = encoding
                self.file['sysencoding'] = sysencoding

        # try to open the file
        inf = codecs.open(infn, 'r', encoding=self.file['encoding'])

        # read in the content and store it
        try:
            data = inf.read()
        except UnicodeDecodeError:
            if self.file['encoding'] == 'ascii':
                logger.warning("suffered UnicodeDecodeError when trying to read file as ascii; trying utf-8")
                inf.close()
                try:
                    inf = codecs.open(infn, 'r', encoding='utf-8')
                except:
                    raise
                else:
                    self.file['sysencoding'] = 'utf-8'
                    data = inf.read()
            else:
                raise
        inf.close()
        self.rawcontent = data
        self.documenturl = 'file://' + self.file['pathgot'].replace(os.pathsep, '/')




