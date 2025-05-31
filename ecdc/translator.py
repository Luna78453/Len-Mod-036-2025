from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ecdc.auth import login_required
from ecdc.db import get_db

bp = Blueprint('translator', __name__)

def shift(_input, shift_amnt):
    _output = chr(ord(_input) + int(shift_amnt)).encode(encoding="utf-8")
    return _output

def encryption(_input, shift_amnt):
    shifted = b''

    for line in _input:
        for char in line:
            shifted = shifted + shift(char, shift_amnt)
    
    return shifted
 
def caesar_encrypt(_in, shifts):
    out = encryption(_in, shifts)

    return out

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        txt = request.form['txt'] 
        txtkey = request.form['txtkey']
        translated_txt = str(caesar_encrypt(txt, txtkey), encoding='utf-8')
        error = None

        if not txt:
            error = 'Text is required.'
        
        if not txtkey:
            error = 'key is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO translation (txt, txtkey, translated_txt, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (txt, txtkey, translated_txt, g.user['id'])
            )
            db.commit()
            return redirect(url_for('translator.index'))
    db = get_db()
    translations = db.execute(
        'SELECT p.id, txt, txtkey, translated_txt, created, author_id, username'
        ' FROM translation p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('translator/index.html', translations=translations)

def get_translation(id, check_author=True):
    translation = get_db().execute(
        'SELECT p.id, txt, txtkey, translated_txt, created, author_id, username'
        ' FROM translation p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if translation is None:
        abort(404, f"translation id {id} doesn't exist.")

    if check_author and translation['author_id'] != g.user['id']:
        abort(403)

    return translation

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_translation(id)
    db = get_db()
    db.execute('DELETE FROM translation WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('translator.index'))
