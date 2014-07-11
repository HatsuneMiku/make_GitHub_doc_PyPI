#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''make_GitHub_doc_PyPI
make GitHub doc PyPI (pydoc to markdown, rst and html)
'''

import sys, os

def getConf(conf_file):
  return open(conf_file, 'rb').read().splitlines()

__conf__ = getConf(os.path.join(os.path.dirname(__file__), 'conf/setup.cf'))
__version__ = __conf__[0]
__url__ = 'https://github.com/HatsuneMiku/make_GitHub_doc_PyPI'
__author__ = '999hatsune'
__author_email__ = '999hatsune@gmail.com'

CONFFILE = u'mkdoc.cf'

def mkdoc_main(basedir):
  cf = os.path.join(basedir, CONFFILE)
  ifp = open(cf, 'rb')
  if ifp is None:
    print u'cannot open %s' % cf
    return
  act, rep = map(lambda s: s.rstrip(), ifp.readlines())
  ifp.close()

if __name__ == '__main__':
  mkdoc_main(os.path.abspath('.'))
