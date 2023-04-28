# -*- coding: utf-8 -*-
import datetime
import subprocess
import os.path
from glob import glob

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
    ("/aoc/", "website/pages/aoc_{}.md"),
    ("/codingcup/", "website/pages/codingcup_{}.md"),
    ("/competitions/", "website/pages/competitions_{}.md"),
    ("/impa/", "website/pages/impa_{}.md"),
    ("/liu-challenge/", "website/pages/liu_challenge_{}.md"),
    ("/ncpc/", "website/pages/ncpc_{}.md"),

    # Misc
    ("/cheats/", "website/pages/cheats_{}.md"),
    ("/git/", "website/pages/git_{}.md"),
]

# Additional main pages


def gamejam_jam_pages():
    # Look for all jam pages in pages/gamejam/jams
    pages = glob("website/pages/gamejam/jams/*")
    bnames = [os.path.basename(page) for page in pages]
    bnames.sort()
    # Jam files are expected to be {year}_{jam}_{lang}.md
    jam_files = [bname.strip(".md").split("_") for bname in bnames]
    for jam in jam_files:
        assert len(jam) == 3, \
            "wrong filename format for a jam: {}".format("_".join(jam))
    # Deduplicate languages
    jams = {}
    for (year, jam, lang) in jam_files:
        key = (year, jam)
        if key not in jams:
            jams[key] = []
        jams[key].append(lang)
    # Check that we have (only) English and Swedish
    for (year, jam), langs in jams.items():
        assert list(sorted(langs)) == ["en", "se"], \
            "jam {} has wrong languages: {}".format(jam, ", ".join(langs))
    return [
        (
            f"/gamejam/jams/{year}-{jam}/",
            f"website/pages/gamejam/jams/{year}_{jam}_{{}}.md"
        )
        for (year, jam) in jams
    ]


# Add the additional main pages
pages += gamejam_jam_pages()

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
