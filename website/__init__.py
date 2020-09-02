# -*- coding: utf-8 -*-
import markdown2

from flask import Flask, render_template, redirect, send_file

app = Flask(__name__, static_folder='static')

# Elements used to create navigation bar
# ((Name_se, Name_en), Url, Internal?)
navigation = [
        (("Start", "Start"),               "/",              True),
        (("Inlägg", "Posts"),              "/posts/",        True),
        (("Kontakt", "Contact us"),        "/contact/",      True),
        (("Tävlingar", "Competitions"),    "/competitions/", True),
        (("Game Jam", "Game Jam"),         "/gamejam/",      True),
        (("Organisation", "Organization"), "/organization/", True),
        (("Fusk", "Cheats"),               "/cheats/",       True)]


def render_page(path, url, nav_index, swedish, injection=""):
    """Render a Markdown file into a page on the website.

    Arguments:
    path - Path to a markdown file.
    url - The url to the page.
    nav_index - Index of page in navigation list.
    swedish - Whether the page is in swedish or not (english).
    """
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


"""Temporary pages
These pages should be removed when apropriate.
"""


"""Redirects
The default page when accessing a link will be in swedish.
"""

@app.route("/")
def index_redir(): return redirect("/se/")

@app.route("/posts/")
def posts_redir(): return redirect("/posts/se/")

@app.route("/contact/")
def contact_redir(): return redirect("/contact/se/")

@app.route("/aoc/")
def aoc_redir(): return redirect("/aoc/se/")

@app.route("/competitions/")
def competitions_redir(): return redirect("/competitions/se/")

@app.route("/organization/")
def organization_redir(): return redirect("/organization/se/")

@app.route("/cheats/")
def cheats_redir(): return redirect("/cheats/se/")

@app.route("/ncpc/")
def ncpc_redir(): return redirect("/ncpc/se/")

@app.route("/impa/")
def impa_redir(): return redirect("/impa/se/")

@app.route("/codingcup/")
def codingcup_redir():
    return redirect("/codingcup/se/")

@app.route("/microjam/")
def microjam_redir():
    return redirect("/microjam/se")

@app.route("/gamejam/")
def gamejam_redir():
    return redirect("/gamejam/se")


"""Pages on sidebar
These pages are shown on and can be accessed from the sidebar.
The render_page is given an index to indicate which link
from the sidebar to highlight.
"""

@app.route("/se/")
def index_se():
    """ Swedish Index page """
    return render_page("website/pages/index_se.md", "/", 0, True)

@app.route("/en/")
def index_en():
    """ English Index page """
    return render_page("website/pages/index_en.md", "/", 0, False)

@app.route("/posts/se/")
def posts_se():
    """ Swedish Posts page """
    return render_page("website/pages/posts_se.md", "/posts/", 1, True)

@app.route("/posts/en/")
def posts_en():
    """ English Posts page """
    return render_page("website/pages/posts_en.md", "/posts/", 1, False)

@app.route("/contact/se/")
def contact_se():
    """ Swedish Contact page """
    return render_page("website/pages/contact_se.md", "/contact/", 2, True)

@app.route("/contact/en/")
def contact_en():
    """ English Contact page """
    return render_page("website/pages/contact_en.md", "/contact/", 2, False)

@app.route("/competitions/se/")
def competitions_se():
    """ Swedish Competitons page """
    return render_page("website/pages/competitions_se.md", "/competitions/", 3, True)

@app.route("/competitions/en/")
def competitions_en():
    """ English Competitons page """
    return render_page("website/pages/competitions_en.md", "/competitions/", 3, False)

@app.route("/gamejam/se/")
def gamejam_se():
    return render_page("website/pages/gamejam_se.md", "/gamejam/", 4, True)

@app.route("/gamejam/en/")
def gamejam_en():
    return render_page("website/pages/gamejam_en.md", "/gamejam/", 4, False)

@app.route("/organization/se/")
def organization_se():
    """ Swedish Organization page """
    return render_page("website/pages/organization_se.md", "/organization/", 5, True)

@app.route("/organization/en/")
def organization_en():
    """ English Organization page """
    return render_page("website/pages/organization_en.md", "/organization/", 5, False)

@app.route("/cheats/se/")
def cheats_se():
    """ Swedish Cheats page """
    return render_page("website/pages/cheats_se.md", "/cheats/", 6, True)

@app.route("/cheats/en/")
def cheats_en():
    """ English Cheats page """
    return render_page("website/pages/cheats_en.md", "/cheats/", 6, False)

"""Other pages
These pages can be accessed from a direct link. They do not show up
on the sidebar. render_page is therefore given the index -1
which results in no page being highlighted on the sidebar.
"""

@app.route("/ncpc/se/")
def ncpc_se():
    """ Swedish NCPC page """
    return render_page("website/pages/ncpc_se.md", "/ncpc/", -1, True)

@app.route("/ncpc/en/")
def ncpc_en():
    """ English NCPC page """
    return render_page("website/pages/ncpc_en.md", "/ncpc/", -1, False)

@app.route("/impa/se/")
def impa_se():
    """ Swedish IMPA page """
    return render_page("website/pages/impa_se.md", "/impa/", -1, True)

@app.route("/impa/en/")
def impa_en():
    """ English IMPA page """
    return render_page("website/pages/impa_en.md", "/impa/", -1, False)

@app.route("/aoc/se/")
def aoc_se():
    """ Swedish Advent of Code page """
    return render_page("website/pages/aoc_se.md", "/aoc/", -1, True,
                       injection=aoc_standings())

@app.route("/aoc/en/")
def aoc_en():
    """ English Advent of Code page """
    return render_page("website/pages/aoc_en.md", "/aoc/", -1, False,
                       injection=aoc_standings())

@app.route("/codingcup/se/")
def codingcup_se():
    """ Swedish Coding Cup page """
    return render_page("website/pages/codingcup_se.md", "/codingcup/", -1, True)

@app.route("/codingcup/en/")
def codingcup_en():
    """ English Coding Cup page """
    return render_page("website/pages/codingcup_en.md", "/codingcup/", -1, False)

@app.route("/microjam/se/")
def microjam_se():
    """ Swedish microjam page """
    return render_page("website/pages/microjam_se.md", "/microjam/", -1, True)

@app.route("/microjam/en/")
def microjam_en():
    """ English microjam page """
    return render_page("website/pages/microjam_en.md", "/microjam/", -1, False)

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
    """ Get the vimrc. """
    return send_file("other/emacs_config", attachment_filename=".emacs", as_attachment=True)

@app.route("/lacc/")
def lacc():
    """ LiTHe kod's Amazing Coding Challenges """
    return static_page("website/other/lacc.html")


def aoc_standings():
    """ Get the current standings in AoC. """
    import json
    with open("aoc_standings.json", "r") as f:
        standings_json = json.loads(f.read())

    contestants = []
    for member_id in standings_json["members"]:
        m = standings_json["members"][member_id]
        if m["name"] is not None:
            contestants.append((int(m["stars"]), int(m["local_score"]), m["name"]))
        else:
            contestants.append((int(m["stars"]), int(m["local_score"]), "Anon." + m["id"]))

    sorting = lambda x: x[0] * 1000 + x[1]
    raised = sum(map(lambda x: x[0] * 10, contestants)) // 2
    placements = [(x[0], x[1][0], x[1][2]) for x in enumerate(sorted(contestants, key=sorting, reverse=True))]
    return render_template("aoc_leaderboard.html",
                           raised=raised,
                           trees=round(raised / 10),
                           contestants=placements)


"""Errorhandlers
For now we only handle pages that are not found.
"""

@app.errorhandler(404)
def not_found(e):
    """ 404 Page """
    return render_page("website/pages/404.md", "/404/", -1, False), 404

@app.route("/404.html")
def not_found_gh_pages():
    """ 404 page to please GitHub pages """
    return render_page("website/pages/404.md", "/404/", -1, False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
