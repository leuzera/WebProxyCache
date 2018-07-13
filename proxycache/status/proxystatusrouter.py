from flask import Flask, render_template
from .cache import Cache

app = Flask(__name__)


@app.route('/')
def hello_name():
    cache = Cache()
    pages = cache.get_pages_num()
    top = cache.get_pages_top()

    return render_template('index.html', nro_pages=pages, pg_access=top)
