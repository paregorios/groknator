#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

module_logger = logging.getLogger('groknator.grokrrrs.base')

class BaseGrokrrr:
    """
    Base grokkr class: everything a baby grokkr needs to know
    """

    def __init__(self):
        self.base = True
        logger = logging.getLogger('groknator.grokrrrs.base.BaseGrokrrr')
        try:
            self.loggers['base'] = logger
        except AttributeError:
            self.loggers = {}
            self.loggers['base'] = logger
