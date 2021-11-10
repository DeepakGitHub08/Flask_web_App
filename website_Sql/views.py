from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import mysql
import MySQLdb.cursors
import json

views = Blueprint('views', __name__);

@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO notes(data, user_id) VALUES (% s, %s)', ( note, current_user.id))
            mysql.connection.commit()
            flash('Note added!', category='success')
   

    return render_template("home.html", user= current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Notes.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})