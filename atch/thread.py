from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from atch.db import get_db
from atch.board import get_all_boards, process_name

bp = Blueprint('thread', __name__)


@bp.route('/<string:uri>/<int:thread>')
def view_thread(uri, thread):
    db = get_db()
    thread_data = db.execute('SELECT * FROM threads WHERE board=? AND thread_id=?', (uri, thread)).fetchone()
    if thread_data is None:
        abort(404)
    replies = db.execute('SELECT * FROM posts WHERE thread=? ORDER BY created', (thread,)).fetchall()

    return render_template('thread.html', thread_data=thread_data, replies=replies, uri=uri,
                           board_list=get_all_boards())


@bp.route('/<string:uri>/<int:thread>/new_post', methods=['POST'])
def new_reply(uri, thread):
    if request.method == 'POST':
        name, tripcode = process_name(request.form['name'])
        email = request.form['email']
        body = request.form['body']
        db = get_db()
        reply_no = len(db.execute("SELECT * FROM posts WHERE thread=? AND board=?", (thread, uri)).fetchall())
        if reply_no == 1000:
            db.execute('UPDATE threads SET archived = 1 WHERE board=? AND thread_id=?',
                       (uri, thread))
        db.execute(
            'INSERT INTO posts (thread, reply_id, name, email, body, board, tripcode) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (thread, reply_no, name, email, body, uri, tripcode)
        )
        if request.form["email"] != "sage":
            db.execute('UPDATE threads SET bump_timestamp = CURRENT_TIMESTAMP WHERE board=? AND thread_id=?',
                       (uri, thread))
        db.commit()
        return redirect(url_for('thread.view_thread', uri=uri, thread=thread))  # view specific post
