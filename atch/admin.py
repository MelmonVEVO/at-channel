import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
from atch.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM admins WHERE username = ?', (username,)
        ).fetchone()

        if (user is None) or (not check_password_hash(user['password'], password)):
            error = 'Incorrect username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))

        flash(error)

    return render_template('login.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
