import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """clear the existing data and create new tables"""
    init_db()
    click.echo('Initialised the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_board)
    app.cli.add_command(get_boards)


@click.command('add_board')
@click.argument('uri')
@click.argument('name')
@with_appcontext
def add_board(uri, name):
    db = get_db()
    db.execute('INSERT INTO boards (uri, name) VALUES (?, ?)', [uri, name])
    db.commit()
    click.echo('Added board /' + uri + "/ - " + name)


@click.command('get_boards')
@with_appcontext
def get_boards():
    boards = get_db().execute('SELECT uri, name FROM boards').fetchall()
    click.echo('All boards: ')
    for b in boards:
        click.echo('/' + b[0] + '/ - ' + b[1])
