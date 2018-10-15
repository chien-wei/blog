from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.db import get_mongo_client
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from flask import Markup

bp = Blueprint('blog', __name__)


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if lang == 'math':
            return '\n%s\n' % mistune.escape(code)
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(linenos='table')
        # other option for formatter: http://pygments.org/docs/formatters/
        return highlight(code, lexer, formatter)


@bp.route('/')
def index():
    client = get_mongo_client()
    db = client.web.posts
    postlist = list(db.find())
    posts = []
    for p in postlist:
        if p['public']:
            posts.append(p)
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    for post in posts:
        post['body'] = Markup(markdown(post['body']))

    return render_template('blog/index.html', posts=posts)


@bp.route('/<url>', methods=('GET', 'POST'))
def page(url):
    client = get_mongo_client()
    db = client.web.posts
    post = db.find_one({'url': url})

    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    post['body'] = Markup(markdown(post['body']))

    return render_template('blog/page.html', post=post)