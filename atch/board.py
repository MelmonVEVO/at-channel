from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
from atch.db import get_db
from hashlib import sha1

bp = Blueprint('board', __name__)


@bp.route('/<string:uri>/')
def browse_board(uri):
    db = get_db()
    board_name = db.execute('SELECT name, uri FROM boards WHERE uri=?', (uri,)).fetchone()
    if board_name is None:
        abort(404)
    threads = db.execute(
        'SELECT threads.thread_id, threads.board, threads.bump_timestamp, threads.title, '
        'posts.created, posts.name, posts.email, posts.body  '
        'FROM threads JOIN posts ON posts.thread=threads.thread_id WHERE threads.board=? and posts.reply_id=0 '
        'ORDER BY bump_timestamp DESC',
        (uri,)
    ).fetchall()

    return render_template('board.html', threads=threads, uri=uri, name=board_name[0], board_list=get_all_boards())


@bp.route('/<string:uri>/new_thread', methods=['POST'])
def new_thread(uri):
    if request.method == 'POST':
        if '◆' in request.form['name']:
            return render_template('post_error.html', why="The diamond symbol (◆) is not allowed in usernames.")
        name = process_name(request.form['name'])
        email = request.form['email']
        title = request.form['title']
        if request.form['body']:
            body = request.form['body']
        else:
            return render_template("post_error.html", why="Your post requires body text.")
        db = get_db()
        thread_number = db.execute('SELECT new_thread_number, uri FROM boards WHERE uri=?', uri).fetchone()[0]
        db.execute('UPDATE boards SET new_thread_number = new_thread_number + 1 WHERE uri=?', uri)
        db.execute(
            'INSERT INTO threads (thread_id, board, title) VALUES (?, ?, ?)',
            (thread_number, uri, title)
        )
        db.execute(
            'INSERT INTO posts (thread, reply_id, name, email, body, board) VALUES (?, 0, ?, ?, ?, ?)',
            (thread_number, name, email, body, uri)
        )
        db.commit()
        return redirect(url_for("thread.view_thread", uri=uri, thread=thread_number))  # view specific post


def get_all_boards():
    db = get_db()
    boards = db.execute('SELECT uri FROM boards').fetchall()
    board_ids = []
    for x in boards:
        board_ids += x[0]
    return board_ids


def process_name(name):
    if name:
        if '#' in name:  # process tripcode
            go = name.index('#')
            trip = sha1(name[go:].encode('utf-8'))
            name = name[:go]
            return name + "◆" + trip.hexdigest()[:10]
    return "Anonymous"
