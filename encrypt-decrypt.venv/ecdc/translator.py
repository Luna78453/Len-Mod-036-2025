from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ecdc.auth import login_required
from ecdc.db import get_db

from caesar import caesar_encrypt

bp = Blueprint('translator', __name__)

@bp.route('/')
def index():
    db = get_db()
    translations = db.execute(
        'SELECT p.id, title, txt, translated_txt, created, author_id, username'
        ' FROM translation p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('translator/index.html', translations=translations)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        txt = request.form['txt'] 
        txtkey = request.form['txtkey']
        translated_txt = caesar_encrypt(txt, txtkey)
        error = None

        if not title:
            error = 'Title is required.'
        
        if not txtkey:
            error = 'key is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO translation (title, txt, txtkey, translated_txt, author_id)'
                ' VALUES (?, ?, ?)',
                (title, txt, txtkey, translated_txt, g.user['id'])
            )
            db.commit()
            return redirect(url_for('translator.index'))

    return render_template('translator/create.html')

def get_translation(id, check_author=True):
    translation = get_db().execute(
        'SELECT p.id, title, txt, txtkey, translated_txt, created, author_id, username'
        ' FROM translation p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if translation is None:
        abort(404, f"translation id {id} doesn't exist.")

    if check_author and translation['author_id'] != g.user['id']:
        abort(403)

    return translation

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    translation = get_translation(id)

    if request.method == 'POST':
        title = request.form['title']
        txt = request.form['txt']
        txtkey = request.form['txtkey']
        translated_txt = caesar_encrypt(txt, txtkey)
        error = None

        if not title:
            error = 'Title is required.'

        if not txtkey:
            error = 'key is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE translation SET title = ?, txt = ?, txtkey = ?, translated_txt = ?'
                ' WHERE id = ?',
                (title, txt, txtkey, translated_txt, id)
            )
            db.commit()
            return redirect(url_for('translator.index'))

    return render_template('translator/update.html', translation=translation)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_translation(id)
    db = get_db()
    db.execute('DELETE FROM translation WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('translator.index'))
