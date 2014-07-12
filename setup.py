from distutils.core import setup
import os

try:
  import pandoc
  nopd = False
  if os.name != 'nt':
    pandoc.core.PANDOC_PATH = 'pandoc'
  else:
    if 'LOCALAPPDATA' in os.environ: app = os.getenv('LOCALAPPDATA')
    else: app = os.getenv('APPDATA')
    pandoc.core.PANDOC_PATH = '%s/Pandoc/pandoc' % (app, )
except (Exception, ), e:
  nopd = True

PKG_TITLE = 'make_GitHub_doc_PyPI'
mdl = __import__(PKG_TITLE)
PKG_VER = mdl.__version__
PKG_URL = mdl.__url__
AUTHOR = mdl.__author__
AUTHOR_EMAIL = mdl.__author_email__
PKG_KWD = '''\
documentation github doc PyPI pydoc markdown rst html'''
PKG_DSC = '''\
make GitHub doc PyPI (pydoc to markdown, rst and html)'''

PYPI_PKGSRC = 'https://pypi.python.org/packages/source'
PYPI_DLURL = '%s/%c/%s/%s-%s.tar.gz' % (
  PYPI_PKGSRC, PKG_TITLE[0], PKG_TITLE, PKG_TITLE, PKG_VER)

long_description = open('README.md', 'rb').read()
if not nopd:
  pd = pandoc.Document()
  pd.markdown = long_description
  long_description = pd.rst

pkg_requirements = map(lambda a: a.split('>')[0],
  open('requirements.txt', 'rb').read().splitlines())

data_apdx = [
  'MANIFEST.in',
  '.gitignore',
  'README.md',
  'mkdoc.py',
  'pre_convert_md_rst_html.py',
  'requirements.txt'
]

R_APDX = [('pre', [
  'css_head.html'
])]
'''
R_APDX += [('%s/%s' % (R_APDX[0][0], 'css'), [
  'docutils.css',
  'pygments.css',
  'pypi.css',
  'pypi-screen.css',
  'styles.css'
])]
'''
data_r_apdx = [map(lambda a: '%s/%s' % (t[0], a), t[1]) for t in R_APDX]

if os.name != 'nt':
  apdx_dir = '/opt/%s' % (PKG_TITLE, ) # setup as data_files
  pkg_apdx = []
else: # to avlid SandboxViolation on mkdir
  apdx_dir = 'conf/%s' % (PKG_TITLE, ) # setup as package_data
  '''
  pkg_apdx = map(lambda a: '%s/%s' % (apdx_dir, a),
    reduce(lambda a, b: a + b, data_r_apdx, data_apdx))
  '''
  pkg_apdx = []

package_data = {
  PKG_TITLE: [
    'conf/template_preview.tar.gz',
    'conf/setup.cf'
  ] + pkg_apdx
}

kwargs = {
  'name'            : PKG_TITLE,
  'version'         : PKG_VER,
  'keywords'        : PKG_KWD,
  'description'     : (PKG_DSC),
  'long_description': long_description,
  'author'          : AUTHOR,
  'author_email'    : AUTHOR_EMAIL,
  'url'             : PKG_URL,
  'download_url'    : PYPI_DLURL,
  'packages'        : [PKG_TITLE],
  'package_dir'     : {PKG_TITLE: './%s' % PKG_TITLE},
  'package_data'    : package_data,
  'requires'        : pkg_requirements,
  'license'         : 'BSD License',
  'classifiers'     : [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 2 :: Only',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ]
}

if os.name != 'nt':
  kwargs['data_files'] = reduce(
    lambda a, b: a + [('%s/%s' % (apdx_dir, R_APDX[b][0]), data_r_apdx[b])],
    range(len(R_APDX)), [(apdx_dir, data_apdx)])

setup(**kwargs)