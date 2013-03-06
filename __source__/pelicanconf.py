#!/usr/bin/env python
# -*- coding: utf-8 -*- #

SITEURL = 'http://danielfrg.github.com'
AUTHOR = u'Daniel Rodriguez'
SITENAME = u'Daniel Rodriguez'
TIMEZONE = 'America/Regina'
DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 5
MARKUP = ('md', 'ipynb')
DEFAULT_DATE_FORMAT = '%B %d, %Y'

THEME = "./themes/subtle/"
STATIC_PATHS = ["images", ]

SITEMAP = {
    'format': 'xml'
}
PLUGINS = ['pelican.plugins.assets', 'pelican.plugins.sitemap']

GOOGLE_ANALYTICS = 'UA-35523657-2'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

PAGE_URL = '/{slug}'
PAGE_SAVE_AS = '/{slug}/index.html'

FILES_TO_COPY = (('robots.txt', 'robots.txt'),
                 ('googleaa9959ae757fe3e1.html', 'googleaa9959ae757fe3e1.html'),
                 ('favicon.ico', 'favicon.ico'),)

