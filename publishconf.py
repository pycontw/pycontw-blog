# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401, E402, F403

SITEURL = "https://conf.python.tw"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = False

EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
}
# Following items are often useful when publishing
GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS")
PLUGINS += ["pelican.plugins.seo"]  # noqa: F405
