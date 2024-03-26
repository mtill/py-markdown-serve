from flask import Flask, send_from_directory
from markdown_it import MarkdownIt
import os
import html
from pathlib import Path


SERVE_DIR = os.environ.get("MARKDOWN_SERVE_DIR", ".")
HIDE_DOTFILES = os.environ.get("MARKDOWN_SERVE_HIDE_DOTFILES", "True") == "True"

app = Flask(__name__)
md = MarkdownIt()
SERVE_PATH = Path(SERVE_DIR).absolute()

def htmlresponse(title, content):
    return """<!DOCTYPE html>

<html>
 <head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>""" + html.escape(title) + """</title>
 </head>
 <body>\n""" + content + """
 </body>
</html>
"""


@app.route('/<path:mypath>.md')
def serve_markdown(mypath):
    thefile = SERVE_PATH / (mypath + ".md")
    with open(thefile, encoding="utf-8") as fp:
        mdrender = md.render(fp.read())
    return htmlresponse(title=mypath, content=mdrender)

@app.route('/', defaults={'mypath': ''})
@app.route('/<path:mypath>')
def serve_others(mypath):
    p = SERVE_PATH / mypath
    if not p.is_relative_to(SERVE_PATH):
        return "access denied."

    if p.is_dir():
        folders = []
        files = []
        for child in p.iterdir():
            if HIDE_DOTFILES and child.name.startswith("."):
                continue
            if child.is_dir():
                folders.append(child.name)
            else:
                files.append(child.name)

        folders.sort()
        files.sort()
        entries = []
        if SERVE_PATH != p:
            entries.append(" <li>📁 <a href=\"../\">../</a></li>")

        for the_folder in folders:
            entries.append(" <li>📁 <a href=\"./" + html.escape(the_folder) + "/\">" + html.escape(the_folder) + "/</a></li>")
        for the_file in files:
            entries.append(" <li>📄 <a href=\"./" + html.escape(the_file) + "\">" + html.escape(the_file) + "</a></li>")

        content = '<ul>\n' + ("\n".join(entries)) + "\n</ul>\n"
        return htmlresponse(title=mypath, content=content)
    else:
        return send_from_directory(str(SERVE_PATH), mypath)

if __name__ == '__main__':
    app.run(debug=False, host="127.0.0.1", port=5000)

