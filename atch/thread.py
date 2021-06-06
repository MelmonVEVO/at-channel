from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from atch.db import get_db
from hashlib import sha1
from atch.board import get_all_boards

bp = Blueprint('thread', __name__)


@bp.route('/<string:uri>/<int:thread>')
def view_thread(uri, thread):
    db = get_db()
    thread_data = db.execute('SELECT * FROM threads WHERE board=? and thread_id=?', (uri, thread)).fetchone()
    replies = db.execute('SELECT * FROM posts WHERE thread=? ORDER BY created', (thread,)).fetchall()

    return render_template('thread.html', thread_data=thread_data, replies=replies, uri=uri,
                           board_list=get_all_boards())


@bp.route('/<string:uri>/<int:thread>/new_post', methods=['POST'])
def new_reply(uri, thread):
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            if '#' in name:  # process tripcode
                go = name.index('#')
                trip = sha1(name[go:].encode('utf-8'))
                name = name[:go]
                name = name + "◆" + trip.hexdigest()[:10]
        else:
            name = "Anonymous"

        email = request.form['email']
        body = request.form['body']
        db = get_db()
        reply_no = 1 + len(db.execute("SELECT * FROM posts WHERE thread=?", (thread,)).fetchall())
        db.execute(
            'INSERT INTO posts (thread, reply_id, name, email, body, board) VALUES (?, ?, ?, ?, ?, ?)',
            (thread, reply_no, name, email, body, uri)
        )
        if request.form["email"] != "sage":
            db.execute('UPDATE threads SET bump_timestamp = CURRENT_TIMESTAMP WHERE board=? and thread_id=?',
                       (uri, thread))
        db.commit()
        return redirect(url_for('thread.view_thread', uri=uri, thread=thread))  # view specific post
