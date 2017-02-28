from prj import app
# from prj import dbm
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


@app.route('/')
@app.route('/index')
def index():
    # return "Hello, World!"
    entries = "Hello, World!"
    return render_template('show_entries.html', entries=entries)

