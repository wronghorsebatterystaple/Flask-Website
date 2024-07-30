import bleach
from functools import wraps
import re

from flask import redirect, url_for

from app import db
from app.models import *
import app.util as util


def additional_markdown_processing(s) -> str:
    """Markdown tweaks round 2.

    Changes:
        - Remove extra `<p>` tags generated by 3rd-party extension `markdown_grid_tables` around `<pre>` tags that
          mess up table spacing and don't seem to be JQuery-parsable
    """

    s = s.replace("</pre></p>", "</pre>")
    # using regex to not take chances here with attributes and stuff
    s = re.sub(r"<p><pre([\S\s]*?)>", r"<pre\1>", s)

    return s


def get_blogpage_id(blueprint_name) -> int:
    """Gets blogpage id from `request.blueprint`."""
    return int(blueprint_name.split('.')[-1])


def login_required_check_blogpage(request):
    """Enforces login to access private blogpages."""
    def inner_decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            blogpage = db.session.get(Blogpage, get_blogpage_id(request.blueprint))
            if blogpage is None:
                return redirect(url_for(f"main.index",
                        flash_message=util.encode_URI_component("That blogpage doesn't exist."),
                        _external=True))

            if blogpage.login_required:
                result = util.custom_unauthorized(request)
                if result:
                    return result

            return func(*args, **kwargs)
        return wrapped
    return inner_decorator


def sanitize_untrusted_html(c) -> str:
    """Markdown sanitization for comments (XSS etc.).

    Notes:
        - Bleach is deprecated because html5lib is, but both seem to still be mostly active
    """

    # MathJax is processed client-side after this so no need to allow those tags
    c = bleach.clean(c,
            tags={"abbr", "acronym", "b", "blockquote", "br", "center", "code", "details", "div", "em",
                "h1", "h2", "h3", "i", "li", "p", "pre", "ol", "small", "span", "strong", "sub", "summary",
                "sup", "table", "tbody", "td", "th", "thead", "tr", "ul"},
            attributes=["class", "colspan", "data-align-bottom", "data-align-center", "data-align-right",
                "data-align-top", "data-col-width", "height", "rowspan", "title", "width"])
    return c

def getPostFromURL(URL_post_sanitized_title, URL_blogpage_id):
    """Gets post from URL, making sure it's valid and matches the whole URL."""
    return db.session.query(Post).filter(Post.sanitized_title == URL_post_sanitized_title,
            Post.blogpage_id == URL_blogpage_id).first()
