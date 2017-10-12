from flask import Flask, render_template,send_file
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import sys
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
app = Flask(__name__)
app.config.from_object(__name__)

flatpages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
def index():
    pages = (p for p in flatpages if 'date' in p.meta)
    return render_template('index.html', pages=pages)

@app.route('/pages/<path:path>/')
def page(path):
    print (path)
    page = flatpages.get_or_404(path)
    #t="build/pages/"+path+'/index.html'
    #return send_file(t)
    return render_template('page.html', page=page)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)
