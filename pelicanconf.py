#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'limengyun'
SITENAME = u"limengyun's blog"
SITEURL = 'http://limengyun.com'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('Markdown Syntax', '/pages/markdown-syntax.html'),)

# Social widget
SOCIAL = (('网易惠惠', 'http://huihui.cn/?keyfrom=limengyun.com'),
          ('xiaoshuov', 'http://www.xiaoshuov.com'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

THEME = "themes/notmyidea"

GOOGLE_ANALYTICS = "UA-37781337-1"
#DISQUS_SITENAME = "limengyun"

PLUGIN_PATH = './pelican-plugins'
PLUGINS = ['sitemap',]

SITEMAP = {
    'format': 'xml',
}

FILES_TO_COPY = (('extra/CNAME', 'CNAME'),
		('extra/robots.txt', 'robots.txt'),
		('extra/83305223c55eb57b6c1fa13fc1a835b2.txt', '83305223c55eb57b6c1fa13fc1a835b2.txt')
		)
