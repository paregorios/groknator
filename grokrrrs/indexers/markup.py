#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
indexers for working with markup
"""

import logging
import re

module_logger = logging.getLogger('groknator.grokrrrs.indexers.markup')

DEFAULTVOCABS = {
    "http://purl.org/dc/terms/" : "dcterms",
}



class MarkupIndexer:
    """
    basic indexer class ClassName(object):
    """

    def __init__(self):
        pass

class ElementIndexer(MarkupIndexer):
    """
    foo
    """

    def __init__(self):
        self.logger = logging.getLogger('groknator.grokrrrs.html.ElementIndexer')
        MarkupIndexer.__init__(self)

    def index(self, soup):
        logger = self.logger
        try:
            return self.elements
        except AttributeError:
            pass
        elements = {}
        tagnames = set([t.name.strip() for t in soup.find_all(True)])
        for tagname in tagnames:
            elements[tagname] = {}
            tags = soup.find_all(tagname)
            elements[tagname]['count'] = len(tags)
            elements[tagname]['instances'] = []
            for tag in tags:
                ele = {}
                ele['attributes'] = {}
                for a in sorted(tag.attrs.keys()):
                    val = tag.attrs[a]
                    if type(val) is list:
                        val = u' '.join(val)
                    p = re.compile(u'\s+')
                    val = p.sub(u' ', val).strip()
                    ele['attributes'][a] = val
                t = tag.get_text()
                t = u''.join(t)
                p = re.compile('\s+')
                t = p.sub(u' ', t)
                t = t.strip()
                if len(t) > 0:
                    ele['text'] = t
                elements[tagname]['instances'].append(ele)
        logger.debug("elements: %s" % sorted(elements.keys()))
        self.elements = elements
        return elements

class AttributeIndexer(MarkupIndexer):
    """
    bar
    """

    def __init__(self, element_indexer=None):
        self.logger = logging.getLogger('groknator.grokrrrs.html.AttributeIndexer')
        MarkupIndexer.__init__(self)
        try:
            self.ei = element_indexer
        except:
            pass

    def index(self, soup):
        logger = self.logger
        try:
            return self.attributes
        except:
            pass
        d = {}
        attributes = []
        try:
            tagnames = self.ei.index(soup).keys()
        except:
            tagnames = set([t.name.strip() for t in soup.find_all(True)])
        for tagname in tagnames:
            thesea = [t.attrs for t in soup.find_all(tagname)]
            for thisa in thesea:
                attributes.extend(thisa.keys())
        attributes = set(attributes)
        for attribute in attributes:
            kwt = "%s" % attribute
            logger.debug("kwt: '%s'" % kwt)
            d[kwt] = []
            try:
                attrtags = soup.find_all(True, **{kwt : True})
            except TypeError:
                attrtags = soup.find_all(True)
                attrtags = [attrtag for attrtag in attrtags if kwt in attrtag.attrs.keys()]
            for attrtag in attrtags:
                attrtagname = attrtag.name
                logger.debug("attrtagname: %s" % attrtagname)
                attrtagvalue = attrtag[attribute]
                logger.debug("attrtagvalue: %s" % attrtagvalue)
                if type(attrtagvalue) == list:
                    attrtagvalue = u' '.join(attrtagvalue)
                p = re.compile('\s+')
                attrtagvalue = p.sub(u' ', attrtagvalue)
                dattr = {'element': attrtagname.strip(), 'value': attrtagvalue.strip()}
                d[kwt].append(dattr)
        logger.debug("attributes: %s" % sorted(d.keys()))
        for attr in sorted(d.keys()):
            logger.debug("%s = '%s'" % (attr, d[attr]))
        self.attributes = d
        return d

class RDFaIndexer(MarkupIndexer):
    """
    noodle
    """

    def __init__(self, vocabs=DEFAULTVOCABS, attribute_indexer=None):
        self.logger = logging.getLogger('groknator.grokrrrs.html.RDFaIndexer')
        try:
            self.ai = attribute_indexer
        except:
            pass
        MarkupIndexer.__init__(self)
        self.vocabs = vocabs

    def index(self, soup):
        logger = self.logger
        d = {}
        try:
            attributenames = self.ai.index(soup).keys()
        except:
            self.ai = AttributeIndexer()
            attributenames = self.ai.index(soup).keys()
        logger.debug("attribute names: %s" % attributenames)
        if 'property' in attributenames:
            logger.debug("we might have rdfa in html!")

            # parse out prefixes
            prefixstring = soup.html.get('prefix')
            logger.debug("prefixes: %s" % prefixstring)
            p = re.compile(':\s*')
            prefixstring = p.sub('=', prefixstring.strip())
            logger.debug("prefixes: %s" % prefixstring)
            p = re.compile('http=')
            prefixstring = p.sub('http:', prefixstring)
            logger.debug("prefixes: %s" % prefixstring)
            p = re.compile('https=')
            prefixstring = p.sub('https:', prefixstring)
            logger.debug("prefixes: %s" % prefixstring)
            p = re.compile('\s+')
            prefixstring = p.sub(';', prefixstring)
            logger.debug("prefixes: %s" % prefixstring)
            prefixes = dict(item.split('=') for item in prefixstring.split(';'))
            for k in sorted(prefixes.keys()):
                logger.debug("prefix %s = %s" % (k, prefixes[k]))

            # parse out properties
            proptags = soup.find_all(True, property=True)
            properties = {}
            for proptag in proptags:
                logger.debug("proptag %s" % str(proptag))
                pkey = proptag.get("property")
                prefix, term = pkey.split(':')
                namespace = prefixes[prefix]
                if namespace in self.vocabs.keys():
                    pkey = ':'.join((self.vocabs[namespace], term))
                    pval = proptag.get_text(" ", strip=True).strip()
                    if pkey in properties.keys():
                        properties[pkey].append(pval)
                    else:
                        properties[pkey] = [pval, ]
                else:
                    logger.warning("ignoring RDFa property value of %s because namespace %s does not correspond to a vocabulary recognized by grokler" % (pkey, namespace))
            for k in sorted(properties.keys()):
                logger.debug("property: %s = %s" % (k, properties[k]))
            return properties
        else:
            logger.info("no rdfa detected")

class MetaIndexer(MarkupIndexer):
    """
    whonk
    """

    def __init__(self, element_indexer=None):
        self.logger = logging.getLogger('groknator.grokrrrs.html.MetaIndexer')
        try:
            self.ei = element_indexer
        except:
            pass        
        MarkupIndexer.__init__(self)


    def index(self, soup, document_url):
        logger = self.logger
        try:
            return self.meta
        except:
            pass    

        try:
            metatags = self.ei.index(soup)['meta']['instances']
        except:
            self.ei = ElementIndexer()
            metatags = self.ei.index(soup)['meta']['instances']

        if len(metatags) > 0:
            logger.debug("metatags: %s" % len(metatags))
            properties = {}
            namespace = document_url
            namedmetas = []
            for tag in metatags:
                if 'name' in tag['attributes'].keys():
                    namedmetas.append(tag)
                elif 'http-equiv' in tag['attributes'].keys():
                    namedmetas.append(tag)
                    z = tag['attributes']['http-equiv']
                    namedmetas[-1]['attributes']['name'] = z
            for tag in namedmetas:
                logger.debug("meta: %s" % tag)
                pkey = '#'.join((namespace, tag['attributes']['name']))
                pval = tag['attributes']['content'].strip()
                if pkey in properties.keys():
                        properties[pkey].append(pval)
                else:
                    properties[pkey] = [pval, ]
            for k in sorted(properties.keys()):
                logger.debug("property: %s = %s" % (k, properties[k]))
            return properties
        else:
            logger.info("no meta tags detected")









