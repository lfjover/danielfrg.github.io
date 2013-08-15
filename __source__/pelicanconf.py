# -*- coding: utf-8 -*- #

SITEURL = '/'
SITEURL = 'http://danielfrg.github.io'
AUTHOR = 'Daniel Rodriguez'
SITENAME = 'Daniel Rodriguez'
TIMEZONE = 'America/Regina'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 10
MARKUP = ('md', 'ipynb')
DEFAULT_DATE_FORMAT = '%d.%m.%Y'

PATH = './'
PAGE_DIR = './pages'
ARTICLE_DIR = './articles'

THEME = "./themes/middle/"
STATIC_PATHS = ["images"]

SITEMAP = {
    'format': 'xml'
}

PLUGIN_PATH = './plugins'
PLUGINS = ['sitemap', 'ipythonnb']

GOOGLE_ANALYTICS = 'UA-35523657-2'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

FILES_TO_COPY = (('robots.txt', 'robots.txt'),
                 ('404.html', '404.html'),
                 ('favicon.ico', 'favicon.ico'),
                 ('google_verification.html', 'googleaa9959ae757fe3e1.html'),)
