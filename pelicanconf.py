# Site metadata
AUTHOR = "PyCon Taiwan Organizers"
SITENAME = "PyCon Taiwan Blog"
SITETITLE = "PyCon Taiwan"
SITEDESCRIPTION = "PyCon Taiwan official blog. Catch up the latest announcement here!"
# empty for local development
SITEURL = ""
SITELOGO = SITEURL + "/images/profile.jpg"
# FAVICON = SITEURL + "/images/favicon.ico"


# blog config
PATH = "content"
STATIC_PATHS = ["images", "extra"]
PLUGIN_PATHS = ["plugins"]
DEFAULT_PAGINATION = 10
TIMEZONE = "Asia/Taipei"
DEFAULT_LANG = "zh-TW"
MAIN_MENU = True
MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)


# Blogroll
LINKS = (("Official Website", "http://tw.pycon.org"),)


# Social widget
SOCIAL = (
    ("facebook", "https://www.facebook.com/pycontw"),
    ("instagram", "https://www.instagram.com/pycon.tw/"),
    ("twitter", "https://twitter.com/#!/PyConTW"),
    ("linkedin", "https://www.linkedin.com/company/pycontw/"),
    ("flickr", "https://www.flickr.com/photos/pycon_tw/albums/"),
    ("github", "https://github.com/pycontw"),
    ("youtube", "https://www.youtube.com/c/PyConTaiwanVideo"),
    ("itunes-note", "https://podcasts.apple.com/tw/podcast/pycast/id1559843325"),
    ("spotify", "https://open.spotify.com/show/63C4CNtJywIKizNFHRrIGv"),
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Theme Setting
THEME = "theme/Flex"
PLUGINS = ["i18n_subsites"]
PYGMENTS_STYLE = "default"
# JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
ROWSER_COLOR = "#333"


# License
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa",
}
COPYRIGHT_NAME = "PyCon Taiwan"
COPYRIGHT_YEAR = 2023


# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
