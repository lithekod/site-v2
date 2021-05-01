# -*- coding: utf-8 -*-
import markdown2

from flask import (
    Flask,
    render_template,
    redirect,
    send_file,
    url_for,
)

app = Flask(__name__, static_folder='static')

# ========== Navigation ==========
# Elements used to create navigation bar
# ((Name_se, Name_en), Url, Internal?)
# TODO: remove or change 'Internal'

navigation = [
    (("Start", "Start"),               "/",              True),
    (("Kontakt", "Contact us"),        "/contact/",      True),
    (("Tävlingar", "Competitions"),    "/competitions/", True),
    (("Game Jam", "Game Jam"),         "/gamejam/",      True),
    (("Organisation", "Organization"), "/organization/", True),
    (("Fusk", "Cheats"),               "/cheats/",       True),
]

# ========== Helper functions ==========
# These functions make it easy to render files into pages or
# redirecting to other pages.

def render_page(path, url, swedish, injection=""):
    """Render a Markdown file into a page on the website.

    Arguments:
    path - Path to a markdown file.
    url - The url to the page.
    swedish - Whether the page is in swedish or not (english).
    """
    nav_index = next((i for i, (_, u, _) in enumerate(navigation) if u == url), -1)
    return render_template("page.html",
            html=markdown2.markdown_path(path),
            injection=injection,
            url=url,
            navigation=navigation,
            selected=nav_index,
            swedish=swedish)


def static_page(path):
    """
    Renders a file to a static webpage.
    """
    with open(path) as f:
        return f.read()


def redirect_external(url):
    """Workaround for redirecting to external websites.
    Use 'redirect' for redirecting to pages on the site.

    Arguments:
    url - The url which should be redirected to.
    """
    return render_template("redirect.html", url=url)


def create_view(md_file, url, swedish):
    """ Return a function that returns a page. """
    return lambda: render_page(md_file, url, swedish)


def create_redirect(to):
    """ Return a function that returns a redirect. """
    return lambda: redirect(to)

# ========== Temporary pages ==========
# These pages should be removed when apropriate.


# ========== Redirects ==========
# Redirect to the snake-ribs documentation.

@app.route("/snake-ribs")
@app.route("/snake-ribs/")
def snake_ribs():
    return redirect_external("https://lithekod.github.io/snake-ribs/")

# ========== Pages ==========
# These are the main pages on the LiTHe kod website.

pages = [
    ("/",                 "website/pages/index_{}.md"),
    ("/contact/",         "website/pages/contact_{}.md"),
    ("/competitions/",    "website/pages/competitions_{}.md"),
    ("/gamejam/",         "website/pages/gamejam_{}.md"),
    ("/gamejam/history/", "website/pages/gamejam_history_{}.md"),
    ("/gamejam/tools/",   "website/pages/gamejam_tools_{}.md"),
    ("/organization/",    "website/pages/organization_{}.md"),
    ("/cheats/",          "website/pages/cheats_{}.md"),
    ("/ncpc/",            "website/pages/ncpc_{}.md"),
    ("/impa/",            "website/pages/impa_{}.md"),
    ("/aoc/",             "website/pages/aoc_{}.md"),
    ("/codingcup/",       "website/pages/codingcup_{}.md"),
    ("/microjam/",        "website/pages/microjam_{}.md"),
    ("/meetings/",        "website/pages/meetings_{}.md"),
    ("/git/",             "website/pages/git_{}.md"),
]

for url, md_file in pages:
    swedish_url = url + "se/"
    english_url = url + "en/"

    # Swedish version
    view = create_view(md_file.format("se"), url, True)
    app.add_url_rule(swedish_url, swedish_url, view)

    # English version
    view = create_view(md_file.format("en"), url, False)
    app.add_url_rule(english_url, english_url, view)

    # Redirect /url/ -> /url/se/
    app.add_url_rule(url, url, create_redirect(swedish_url))

# ========== Other pages ==========
# These pages can be accessed from a direct link. They do not show up
# on the sidebar.

@app.route("/gitcheatsheet/")
def gitcheatsheet():
    """ The git cheat-sheet of doom! """
    return static_page("website/other/gitcheatsheet.html")

@app.route("/vimrc")
def vimrc():
    """ Get the vimrc. """
    return send_file("other/vimrc", attachment_filename=".vimrc", as_attachment=True)

@app.route("/emacs_config")
def emacs():
    """ Get the emacs config. """
    return send_file("other/emacs_config", attachment_filename=".emacs", as_attachment=True)

@app.route("/lacc/")
def lacc():
    """ LiTHe kod's Amazing Coding Challenges """
    return static_page("website/other/lacc.html")

# ========== Old redirects ==========
# These pages used to exist, but not anymore. They redirect to the new content
# so old links still work.

@app.route("/posts/")
def posts_index():
    return redirect("/meetings/se/")

@app.route("/posts/se/")
def posts_se():
    return redirect("/meetings/se/")

@app.route("/posts/en/")
def posts_en():
    return redirect("/meetings/en/")

# ========== Errorhandlers ==========
# For now we only handle pages that are not found.

@app.errorhandler(404)
def not_found(e):
    """ 404 Page """
    return render_page("website/pages/404.md", "/404/", False), 404

@app.route("/404.html")
def not_found_gh_pages():
    """ 404 page to please GitHub pages """
    return render_page("website/pages/404.md", "/404/", False)

# ========== Running ==========
# Running this file will allow nonlocal devices to access the page.
# Used when, for example, testing on a phone.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
