import markdown2

from flask import Flask, render_template, redirect

app = Flask(__name__, static_folder='static')

GITHUB_LINK = "https://github.com/lithekod"
BYLAWS_LINK = "https://github.com/lithekod/bylaws/blob/master/stadgar.pdf"
PROTOCOLS_LINK = "https://github.com/lithekod/protocols"

# Elements used to create Navigation bar
# ((Name_se, Name_en), Url, Multi-Language?)
navigation = [
        (("Start", "Start"),           "",             True),
        (("Inlägg", "Posts"),          "/posts",       True),
        (("Kontakt", "Contact us"),    "/contact",     True),
        (("Fusk", "Cheats"),           "/cheats",      True),
        (("NCPC", "NCPC"),             "/ncpc",        True),
        (("Vår Github", "Our Github"), GITHUB_LINK,    False),
        (("Stadgar", "By-laws"),       BYLAWS_LINK,    False),
        (("Protokoll", "Protocols"),   PROTOCOLS_LINK, False)]

def render_page(path, nav_index, swedish):
    """Render a Markdown file into a page on the website
    Arguments:
    path ------- Path to a markdown file (or not.. idk)
    nav_index -- Index of page in navigation list
    swedish ---- Whether the page is in swedish or not (english)
    """
    return render_template("page.html",
            html=markdown2.markdown_path(path),
            navigation=navigation,
            selected=nav_index,
            swedish=swedish)

@app.route("/")
def index():
    """ Redirect the index page to the swedish version of the index page """
    return redirect("/se/", code=302)

@app.route("/se/")
def index_se():
    """ Swedish Index page """
    return render_page("website/pages/index_se.md", 0, True)

@app.route("/en/")
def index_en():
    """ English Index page """
    return render_page("website/pages/index_en.md", 0, False)

@app.route("/posts/se/")
def posts_se():
    """ Swedish Posts page """
    return render_page("website/pages/posts_se.md", 1, True)

@app.route("/posts/en/")
def posts_en():
    """ English Posts page """
    return render_page("website/pages/posts_en.md", 1, False)

@app.route("/contact/se/")
def contact_se():
    """ Swedish Contact page """
    return render_page("website/pages/contact_se.md", 2, True)

@app.route("/contact/en/")
def contact_en():
    """ English Contact page """
    return render_page("website/pages/contact_en.md", 2, False)

@app.route("/cheats/se/")
def cheats_se():
    """ Swedish Contact page """
    return render_page("website/pages/cheats_se.md", 3, True)

@app.route("/cheats/en/")
def cheats_en():
    """ English Contact page """
    return render_page("website/pages/cheats_en.md", 3, False)

@app.route("/ncpc/se/")
def ncpc_se():
    """ Swedish NCPC page """
    return render_page("website/pages/ncpc_se.md", 4, True)

@app.route("/ncpc/en/")
def ncpc_en():
    """ English NCPC page """
    return render_page("website/pages/ncpc_en.md", 4, False)

@app.errorhandler(404)
def not_found(e):
    """ 404 Page """
    return render_page("website/pages/404.md", -1, False), 404
