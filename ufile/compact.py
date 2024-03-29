# -*- coding: utf-8 -*-

"""
pythoncompat
"""

import sys

# -------
# Pythons
# -------

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


# ---------
# Specifics
# ---------

if is_py2:
    import urllib
    import StringIO
    StringIO = BytesIO = StringIO.StringIO

    builtin_str = str
    bytes = str
    str = unicode  # noqa
    basestring = basestring  # noqa
    numeric_types = (int, long, float)  # noqa

    def b(data):
        return data

    def s(data):
        return data

    def u(data):
        return unicode(data, 'unicode_escape')  # noqa

    def url_parse(data):
        return urllib.urlencode(data)

    def quote(data):
        return urllib.quote(data)


elif is_py3:
    from urllib import parse  
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO

    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)

    def b(data):
        if isinstance(data, str):
            return data.encode('utf-8')
        return data

    def s(data):
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return data

    def u(data):
        return data

    def url_parse(data):
        return parse.urlencode(data)

    def quote(data):
        return parse.quote(data)

