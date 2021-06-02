import os
import db
from flask import Flask, g


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app['SECRET_KEY'] = "nya"
    app['DATABASE'] = os.path.join(app.instance_path, 'atch.sqlite')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_db()

    g.boards = db.get_db().execute('SELECT uri FROM boards').fetchall()


def get_boards():
    pass
