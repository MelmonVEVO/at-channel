import os
from . import db, board, thread, index
from flask import Flask, render_template, current_app


def four_oh_four(e):
    return render_template('404.html'), 404


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="nya",
        DATABASE=os.path.join(app.instance_path, "atch.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(board.bp)
    app.register_blueprint(thread.bp)
    app.register_blueprint(index.bp)
    app.register_error_handler(404, four_oh_four)

    return app


def get_boards():
    pass
