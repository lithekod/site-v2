# -*- coding: utf-8 -*-
import datetime
import subprocess
from glob import glob
from os.path import basename

import markdown2

from flask import (
    Flask,
    render_template,
    redirect,
    send_file,
    url_for,
)

app = Flask(__name__, static_folder="static")

# ========== Navigation ==========
# Elements used to create navigation bar
# ((name_se, name_en), url)

navigation = [
    (("Start", "Start"), "/"),
    (("Kontakt", "Contact us"), "/contact/"),
    (("Advent of Code", "Advent of Code"), "/aoc/"),
    (("Tävlingar", "Competitions"), "/competitions/"),
    (("Game Jam", "Game Jam"), "/gamejam/"),
    (("Organisation", "Organization"), "/organization/"),
    (("Fusk", "Cheats"), "/cheats/"),
]

# ========== Helper functions ==========
# These functions make it easy to render files into pages or
# redirecting to other pages.


def last_updated(path):
    """Return the author date of the latest commit that touched a path."""
    # %at is author time as unix timestamp
    git_cmd = "git log --format=%at -- {}".format(path).split()
    stdout = subprocess.run(git_cmd, capture_output=True).stdout
    ts = stdout.split(b"\n")[0]
    if ts:
        return datetime.datetime.fromtimestamp(int(ts)).date().isoformat()
    else:
        return "<no commit found>"


def render_page(path, url, swedish, injection=""):
    """Render a Markdown file into a page on the website.

    Arguments:
    path - Path to a markdown file.
    url - The url to the page.
    swedish - Whether the page is in swedish or not (english).
    """
    nav_index = next(
        (i for i, (_, u) in enumerate(navigation) if u == url), -1)
    return render_template(
        "page.html",
        html=markdown2.markdown_path(path),
        injection=injection,
        last_updated=last_updated(path),
        url=url,
        navigation=navigation,
        selected=nav_index,
        swedish=swedish,
    )


def pages_in_dir(url_dir, dir, recurse=False):
    """Return all pages in a directory.
    """
    assert not recurse, "not supported yet"

    # Files are expected to be {slug}_{lang}.md
    files = []
    for path in glob(dir):
        *slug, lang = basename(path).strip(".md").split("_")
        files.append((path, "-".join(slug), lang))
    langs = {}
    paths = {}
    for (path, slug, lang) in files:
        if slug not in langs:
            langs[slug] = []
            paths[slug] = path
        langs[slug].append(lang)
    # Check that we have (only) English and Swedish
    for slug, langs in langs.items():
        assert list(sorted(langs)) == ["en", "se"], \
            "{} has wrong languages: {}".format(paths[slug], ", ".join(langs))
    return [
        (
            f"{url_dir}{slug}/",
            path.removesuffix("_en.md").removesuffix("_se.md") + "_{}.md"
        )
        for (slug, path) in paths.items()
    ]


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
    """Return a function that returns a page."""
    return lambda: render_page(md_file, url, swedish)


def create_redirect(to):
    """Return a function that returns a redirect."""
    return lambda: redirect(to)


# ========== Temporary pages ==========
# These pages should be removed when appropriate.


# EXAMPLE:
"""
@app.route("/opera")
@app.route("/opera/")
def julstuga():
    return redirect_external("https://forms.gle/VeZVCbgEBGiE85mL7")
"""


# ========== Redirects ==========


# Redirect to the snake-ribs documentation.
@app.route("/snake-ribs")
@app.route("/snake-ribs/")
def snake_ribs():
    return redirect_external("https://lithekod.github.io/snake-ribs/")


# Redirect /competitions/ncpc to the latest ncpc page.
def get_latest_ncpc():
    return basename(sorted(glob("website/pages/competitions/ncpc/*_se.md"))[-1]).strip("_se.md")


@app.route("/competitions/ncpc/")
def latest_ncpc():
    return redirect("/competitions/ncpc/se/")


@app.route("/competitions/ncpc/se/")
def latest_ncpc_se():
    return redirect("/competitions/ncpc/{}/se/".format(get_latest_ncpc()))


@app.route("/competitions/ncpc/en/")
def latest_ncpc_en():
    return redirect("/competitions/ncpc/{}/en/".format(get_latest_ncpc()))


# ========== Pages ==========
# These are the main pages on the LiTHe kod website.

pages = [
    # Board
    ("/", "website/pages/index_{}.md"),
    ("/contact/", "website/pages/contact_{}.md"),
    ("/meetings/", "website/pages/meetings_{}.md"),
    ("/organization/", "website/pages/organization_{}.md"),

    # Gamejam
    ("/gamejam/", "website/pages/gamejam/index_{}.md"),
    ("/gamejam/jams/", "website/pages/gamejam/jams_{}.md"),
    ("/gamejam/tools/", "website/pages/gamejam/tools_{}.md"),

    # Hardware
    ("/lodol/", "website/pages/lodol_{}.md"),

    # Competetive programming
    ("/competitions/", "website/pages/competitions/index_{}.md"),
    ("/competitions/aoc/", "website/pages/competitions/aoc_{}.md"),
    ("/competitions/codingcup/", "website/pages/competitions/codingcup_{}.md"),
    ("/competitions/impa/", "website/pages/competitions/impa_{}.md"),
    ("/competitions/liu-challenge/", "website/pages/competitions/liu_challenge_{}.md"),

    # Misc
    ("/cheats/", "website/pages/cheats_{}.md"),
    ("/git/", "website/pages/git_{}.md"),
]


# Add the additional main pages
pages += pages_in_dir("/gamejam/jams/", "website/pages/gamejam/jams/*")
pages += pages_in_dir(
    "/competitions/ncpc/",
    "website/pages/competitions/ncpc/*"
)

# Render the main pages
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
    """The git cheat-sheet of doom!"""
    return static_page("website/other/gitcheatsheet.html")


@app.route("/vimrc")
def vimrc():
    """Get the vimrc."""
    return send_file("other/vimrc", attachment_filename=".vimrc", as_attachment=True)


@app.route("/emacs_config")
def emacs():
    """Get the emacs config."""
    return send_file(
        "other/emacs_config", attachment_filename=".emacs", as_attachment=True
    )


@app.route("/lacc/")
def lacc():
    """LiTHe kod's Amazing Coding Challenges"""
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
    """404 Page"""
    return render_page("website/pages/404.md", "/404/", False), 404


@app.route("/404.html")
def not_found_gh_pages():
    """404 page to please GitHub pages"""
    return render_page("website/pages/404.md", "/404/", False)


# ========== Running ==========
# Running this file will allow nonlocal devices to access the page.
# Used when, for example, testing on a phone.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
