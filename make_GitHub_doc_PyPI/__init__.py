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

import re
import pydoc
import pandoc

CONFFILE = u'mkdoc.cf'

if os.name != 'nt':
  pandoc.core.PANDOC_PATH = 'pandoc'
else:
  if 'LOCALAPPDATA' in os.environ: app = os.getenv('LOCALAPPDATA')
  else: app = os.getenv('APPDATA')
  pandoc.core.PANDOC_PATH = '%s/Pandoc/pandoc' % (app, )

def mkdoc(basedir, mdlname):
  r = re.compile(r'''(https://[^\s\']+)''', re.I)
  fn = 'module_%s' % mdlname
  txt = pydoc.TextDoc().docmodule(__import__(mdlname))
  md = []
  flg = False
  for line in txt.splitlines():
    if flg:
      flg = False
      continue
    outl = []
    f = False
    for i, l in enumerate(line):
      if l == '\x08':
        if i <= 1: f = True
        outl = outl[:-1]
      else:
        outl += [l]
    outline = ''.join(outl)
    if outline == 'FILE':
      flg = True
    else:
      #outline = r.sub(lambda m: '[%s](%s)' % (m.group(1), m.group(1)), outline)
      md += ['%s%s' % ('# ' if f else '', outline)]
  open(os.path.join(basedir, '%s.md' % fn), 'wb').write('\x0A'.join(md))

  # Do not use output of pydoc.HTMLDoc() because of poor design.
  # So convert to html from markdown created above.
  pd = pandoc.Document()
  pd.markdown = '\x0A'.join(md)
  open(os.path.join(basedir, '%s.html' % fn), 'wb').write(pd.html)

def mkdoc_main(basedir):
  cf = os.path.join(basedir, CONFFILE)
  ifp = open(cf, 'rb')
  if ifp is None:
    print u'cannot open %s' % cf
    return
  act, rep = map(lambda s: s.rstrip(), ifp.readlines())
  ifp.close()
  mkdoc(rep)

if __name__ == '__main__':
  mkdoc_main(os.path.abspath('.'))
