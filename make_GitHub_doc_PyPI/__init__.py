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
import tarfile
import pydoc
import pandoc

CONFFILE = u'mkdoc.cf'
TEMPLATE_PREVIEW = 'conf/template_preview.tar.gz'
OUTDIR = u'/tmp/preview_mkdoc'
CSS_HEAD = 'pre/css_head.html'
CODE_REPLACEMENTS = [
  ('sourceCode python', 'literal-block'),
  ('sourceCode bash', 'literal-block'),
  ('<pre><code>', '<pre class="literal-block"><code>')]

def initPandoc():
  if os.name != 'nt':
    pandoc.core.PANDOC_PATH = 'pandoc'
  else:
    if 'LOCALAPPDATA' in os.environ: app = os.getenv('LOCALAPPDATA')
    else: app = os.getenv('APPDATA')
    pandoc.core.PANDOC_PATH = '%s/Pandoc/pandoc' % (app, )

def openHTML(dst):
  if os.name != 'nt':
    import subprocess
    p = subprocess.Popen(['lynx %s' % (dst, )], 4096, None,
      None, None, None, # subprocess.PIPE, subprocess.PIPE, subprocess.PIPE
      preexec_fn=None, close_fds=False, shell=True)
    p.wait()
  else:
    import win32com.client
    ie = win32com.client.Dispatch('InternetExplorer.Application')
    ie.Visible = True
    ie.Navigate(re.sub(re.compile(r'\/', re.I), r'\\', dst))
    ie.Quit()

def extract_html(fname, str_html):
  if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    if not os.path.exists(OUTDIR):
      print u'cannot create %s' % OUTDIR
      return
  tf = os.path.join(os.path.dirname(__file__), TEMPLATE_PREVIEW)
  tarfile.open(tf, 'r:gz').extractall(OUTDIR)
  head = open(os.path.join(OUTDIR, CSS_HEAD), 'rb').read()
  out_html = '%s\n%s' % (head, str_html)
  dst = os.path.join(OUTDIR, 'pre/%s' % fname)
  f = open(dst, 'wb')
  f.write(out_html)
  f.close()
  openHTML(dst)

def md_to_html(str_md):
  # Do not use output of pydoc.HTMLDoc() because of poor design.
  # So convert to html from markdown created above.
  initPandoc()
  md = pandoc.Document()
  md.markdown = str_md
  pd = pandoc.Document()
  pd.rst = md.rst
  out_html = pd.html
  rpls = map(lambda a: (re.compile(a[0], re.M|re.S), a[1]), CODE_REPLACEMENTS)
  for rpl in rpls:
    out_html = re.sub(rpl[0], rpl[1], out_html)
  return out_html

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
  out_md = '\x0A'.join(md)
  open(os.path.join(basedir, '%s.md' % fn), 'wb').write(out_md)
  extract_html('%s.html' % fn, md_to_html(out_md))

def mkdoc_main(basedir):
  cf = os.path.join(basedir, CONFFILE)
  ifp = open(cf, 'rb')
  if ifp is None:
    print u'cannot open %s' % cf
    return
  act, rep = map(lambda s: s.rstrip(), ifp.readlines())
  ifp.close()
  mkdoc(basedir, rep)

if __name__ == '__main__':
  mkdoc_main(os.path.abspath('.'))
