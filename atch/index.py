from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
from atch.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    db = get_db()
    boards = db.execute(
        'SELECT uri, name FROM  boards ORDER BY uri'
    ).fetchall()

    return render_template('index.html', boards=boards)
