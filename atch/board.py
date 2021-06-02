from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from atch.db import get_db
from hashlib import sha1

bp = Blueprint('board', __name__)


@bp.route('/<string:uri>/<int:page>')
def browse_board(uri, page):
    db = get_db()
    threads = db.execute(
        'SELECT thread, thread_pos, board, created, op, email, title, body '
        'FROM posts WHERE board == ? '
        'ORDER BY created DESC',
        uri
    ).fetchmany(5 + 5 * page)

    return render_template('board.html', threads=threads)


@bp.route('/<string:uri>/new_thread', methods=['GET', 'POST'])
def new_thread(uri):
    if request.method == 'POST':
        op = ""
        if request.form['op']:
            op = request.form['op']
            if '#' in op:  # process tripcode
                go = op.index('#')
                trip = sha1(op[go:].encode('utf-8'))
                op = op[:go]
                op = op + "◆" + trip.hexdigest()[:10]
        else:
            op = "Anonymous"
        email = request.form['email']
        title = request.form['title']
        body = request.form['body']
        db = get_db()
        thread_number = db.execute('SELECT new_thread_number, uri FROM boards WHERE uri == ?', uri)
        db.execute('UPDATE boards SET new_thread_number = new_thread_number + 1 WHERE uri == ?', uri)
        db.execute(
            'INSERT INTO posts (thread, thread_pos, board, op, email, title, body) VALUES (?, 0, ?, ?, ?, ?, ?)',
            [thread_number[0], uri, op, email, title, body]
        )
        db.commit()

    abort(403)
