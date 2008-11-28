from web.template import CompiledTemplate, ForLoop


def archive():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__(rows):
        yield '', join_('\n')
        yield '', join_('<ul class="posts">\n')
        yield '', join_('<h1>Archive</h1>\n')
        for row in loop.setup(rows):
            yield '', join_('<li><span>', escape_(row.pub_date[:10], True), '</span> &raquo; <a href="/', escape_(row.url, True), '">', escape_(row.title, True), '</a></li>\n')
        yield '', join_('</ul>')
    return __template__

archive = CompiledTemplate(archive(), 'templates/archive.html')


def login():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__():
        yield '', join_('\n')
        yield '', join_('<form id="form" action="/login" method="post"> \n')
        yield '', join_("    <label for='username'>User Name</label><br/>\n")
        yield '', join_('    <input type=\'text\' name=\'username\' id=\'username\' class="w-50"/><br/>\n')
        yield '', join_("    <label for='password'>Password</label><br/>\n")
        yield '', join_('    <input type=\'password\' name=\'password\' id=\'password\'  class="w-50"/><br/>\n')
        yield '', join_('    <br/>\n')
        yield '', join_('    <input type="submit" value="Publish Page" /> \n')
        yield '', join_('</form>')
    return __template__

login = CompiledTemplate(login(), 'templates/login.html')


def base():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (header, footer, page, site_globals=None, register_script=None):
        yield '', join_('\n')
        yield '', join_('<html>\n')
        yield '', join_('    <head>\n')
        yield '', join_('        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        yield '', join_('        <title>\n')
        if site_globals:
            yield '', join_('        ', escape_(site_globals.title, True), '\n')
        yield '', join_('        </title>\n')
        yield '', join_('        <link rel="stylesheet" href="/static/css/screen.css" type="text/css" media="screen, projection" />\n')
        yield '', join_('        <link rel="shorcut icon" href="/static/media/favicon.ico"/> \n')
        yield '', join_('        <link rel="alternate" type="application/rss+xml" title="RSS Feed" href="/feed/rss2" />\n')
        yield '', join_('        <script type="text/javascript" src="/static/js/jquery.js"></script>\n')
        yield '', join_('        <script type="text/javascript" src="/static/js/jquery.form.js"></script>\n')
        yield '', join_('        <script type="text/javascript" src="/static/js/jquery.player.js"></script>\n')
        yield '', join_('    </head>\n')
        yield '', join_('\n')
        yield '', join_('    <body>\n')
        yield '', join_('        <div class="site">\n')
        yield '', join_('            ', escape_(header, False), '\n')
        yield '', join_('            ', escape_(page, False), '\n')
        yield '', join_('            ', escape_(footer, False), '\n')
        yield '', join_('        </div>\n')
        if register_script:
            yield '', join_('        ', "<script type='text/javascript'>\n")
            yield '', join_('        ', escape_(register_script, False), '\n')
            yield '', join_('        ', '</script>\n')
        yield '', join_('    </body>\n')
        yield '', join_('</html>')
    return __template__

base = CompiledTemplate(base(), 'templates/base.html')


def post():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (record, related=None):
        yield '', join_('\n')
        if record:
            yield '', join_('<div id="post">\n')
            yield '', join_('    <h1>', escape_(record.title, True), '</h1>\n')
            yield '', join_('    <p class="meta">', escape_(record.author, True), ' &mdash; ', escape_(record.pub_date[:10], True), '</p>\n')
            yield '', join_('    <p>', escape_(record.content, False), '</p>\n')
            yield '', join_('</div>\n')
            yield '', join_('\n')
            yield '', join_('<div id="related">\n')
            if related:
                yield '', join_('<h2>Related Posts</h2>\n')
                yield '', join_('<ul class="posts">\n')
                for object in loop.setup(related):
                    yield '', join_('<li><span>', escape_(object.pub_date, True), '</span> &raquo; <a href="/', escape_(object.url, True), '">', escape_(object.title, True), '</a></li>\n')
                yield '', join_('</ul>\n')
            yield '', join_('</div>')
    return __template__

post = CompiledTemplate(post(), 'templates/post.html')


def notfound():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (url=None):
        yield '', join_('\n')
        yield '', join_('<h1 style="color:#a00">404 Error</h1>\n')
        yield '', join_('\n')
        yield '', join_('URL: <code>/', escape_(url, True), '</code>')
    return __template__

notfound = CompiledTemplate(notfound(), 'templates/notfound.html')


def home():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (sections):
        yield '', join_('\n')
        yield '', join_('<div id="home">\n')
        for section in loop.setup(sorted(sections.keys())):
            yield '', join_('    ', '<h1>', escape_(section, True), '</h1>\n')
            yield '', join_('    ', '    <ul class="posts">\n')
            for entry in loop.setup(sections[section]):
                yield '', join_('        ', '<li><span>', escape_(entry.pub_date[:10], True), '</span> &raquo; <a href="/', escape_(entry.url, True), '">', escape_(entry.title, True), '</a></li>\n')
            yield '', join_('    ', '    </ul>\n')
        yield '', join_('</div>')
    return __template__

home = CompiledTemplate(home(), 'templates/home.html')


def rss2():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__(feed):
        yield '', join_(escape_(feed, False))
    return __template__

rss2 = CompiledTemplate(rss2(), 'templates/rss2.html')


def edit():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (url, key_name=None):
        yield '', join_('\n')
        yield '', join_('<form id="form" action="', escape_(url, True), '" method="post"> \n')
        yield '', join_("    <label for='title'>Title</label><br/>\n")
        yield '', join_("    <input type='text' name='title' id='title' /><br/>\n")
        yield '', join_("    <label for='content'>Content</label><br/>\n")
        yield '', join_('    <textarea name="content" id="content"></textarea> <br/>\n')
        yield '', join_("    <label for='url'>URL</label><br/>\n")
        yield '', join_("    <input type='text' name='url' id='url' /><br/>\n")
        yield '', join_("    <label for='section'>Section</label><br/>\n")
        yield '', join_("    <input type='text' name='section' id='section' /><br/>\n")
        yield '', join_("    <label for='author'>Author</label><br/>\n")
        yield '', join_("    <input type='text' name='author' id='author' /><br/>\n")
        yield '', join_('    <input type=\'hidden\' name=\'key_name\' id=\'key_name\' value="', escape_(key_name, True), '"/>\n')
        yield '', join_("    <input type='hidden' name='pub_date' id='pub_date' />\n")
        yield '', join_('<br/>\n')
        yield '', join_('    <input type="submit" value="Save Changes" /> \n')
        yield '', join_('    <a href="#" id="delete" class="delete">Delete Page</a>\n')
        yield '', join_('</form>\n')
        yield '', join_('\n')
        yield '', join_('<script type="text/javascript" src="/static/js/wymeditor/jquery.wymeditor.js"></script>\n')
        yield '', join_('<script type="text/javascript" src="/static/js/edit.js"></script>')
    return __template__

edit = CompiledTemplate(edit(), 'templates/edit.html')


def editor():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (header, footer, page, site_globals=None, register_script=None):
        yield '', join_('\n')
        yield '', join_('<html>\n')
        yield '', join_('    <head>\n')
        yield '', join_('        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        yield '', join_('        <title>\n')
        if site_globals:
            yield '', join_('        ', escape_(site_globals.title, True), '\n')
        yield '', join_('        </title>\n')
        yield '', join_('        <link rel="stylesheet" href="/static/css/screen.css" type="text/css" media="screen, projection" />\n')
        yield '', join_('        <link rel="shorcut icon" href="/static/media/favicon.ico"/> \n')
        yield '', join_('        <script type="text/javascript" src="/static/js/jquery.js"></script>\n')
        yield '', join_('        <script type="text/javascript" src="/static/js/jquery.form.js"></script>\n')
        yield '', join_('    </head>\n')
        yield '', join_('\n')
        yield '', join_('    <body>\n')
        yield '', join_('        <div class="site editor">\n')
        yield '', join_('            ', escape_(header, False), '\n')
        yield '', join_('            ', escape_(page, False), '\n')
        yield '', join_('            ', escape_(footer, False), '\n')
        yield '', join_('        </div>\n')
        if register_script:
            yield '', join_('        ', "<script type='text/javascript'>\n")
            yield '', join_('        ', escape_(register_script, False), '\n')
            yield '', join_('        ', '</script>        \n')
        yield '', join_('    </body>\n')
        yield '', join_('</html>')
    return __template__

editor = CompiledTemplate(editor(), 'templates/editor.html')


def delete():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__(url):
        yield '', join_('\n')
        yield '', join_("<form method='post' action='/delete/", escape_(url, True), "'>\n")
        yield '', join_('    <h2>Delete Object</h2>\n')
        yield '', join_('    <p>\n')
        yield '', join_('        Requested object: <code>/', escape_(url, True), '</code></p>\n')
        yield '', join_('\n')
        yield '', join_('    <p class="warn">\n')
        yield '', join_('        Warning: delete operation is irreversible. </p>\n')
        yield '', join_("    <input type='submit' value='Yes, I am certain about this'>\n")
        yield '', join_('</form>')
    return __template__

delete = CompiledTemplate(delete(), 'templates/delete.html')


def header():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (site_globals, superuser=None, view_editor=None):
        yield '', join_('\n')
        yield '', join_('<div class="title">\n')
        yield '', join_('    <a href="/">', escape_(site_globals.site_name, True), '</a>\n')
        yield '', join_('    <a class="extra" href="/">home</a>\n')
        yield '', join_('    <span>&middot;</span>\n')
        yield '', join_('    <a class="extra" href="/archive">archive</a>\n')
        if superuser:
            yield '', join_('    ', '<span>&middot;</span>\n')
            if view_editor:
                yield '', join_('    ', '<a class="extra" href="/edit', escape_(site_globals.ctx.path, True), '">edit page &para;</a>\n')
                yield '', join_('    ', '<span>&middot;</span>\n')
            yield '', join_('    ', '<a class="extra" href="/add/new">new page</a>\n')
            yield '', join_('    ', '<span>&middot;</span>\n')
            yield '', join_('    ', '<a class="extra" href="/logout">logout</a>\n')
        yield '', join_('</div>\n')
    return __template__

header = CompiledTemplate(header(), 'templates/header.html')


def footer():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (foo=None):
        yield '', join_('\n')
        yield '', join_('<div class="footer">\n')
        yield '', join_('    <div class="contact">\n')
        yield '', join_('      <p>\n')
        yield '', join_('        Tzury Bar Yochay<br/>\n')
        yield '', join_('        <a href="mailto:tzury.by@gmail.com">tzury.by@gmail.com</a><br/>\n')
        yield '', join_('        Design by <a href="http://tom.preston-werner.com/"> Tom Preston-Werner</a>\n')
        yield '', join_('      </p>\n')
        yield '', join_('    </div>\n')
        yield '', join_('    <div class="contact">\n')
        yield '', join_('      <p>\n')
        yield '', join_('        <a href="http://www.facebook.com/people/Tzury_Bar_Yochay/513676303">facebook.com</a><br/>\n')
        yield '', join_('        <a href="http://evalinux.wordpress.com/">evalinux.wordpress.com</a><br/>\n')
        yield '', join_('        <a href="http://twitter.com/tzury">twitter.com/tzury</a>\n')
        yield '', join_('      </p>\n')
        yield '', join_('    </div>\n')
        yield '', join_('    <div class="rss">\n')
        yield '', join_('      <a href="/feed/rss2">\n')
        yield '', join_('        <img alt="Subscribe to RSS Feed" src="/static/media/rss.png"/>\n')
        yield '', join_('      </a>\n')
        yield '', join_('    </div>\n')
        yield '', join_('</div>        \n')
    return __template__

footer = CompiledTemplate(footer(), 'templates/footer.html')

