from flask import Blueprint, render_template, request, flash, jsonify,session
from . import mysql
import MySQLdb.cursors
import json

views = Blueprint('views', __name__);

@views.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO notes(data, user_id) VALUES (% s, %s)', ( note, session['id']))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM notes WHERE user_id = %(user_id)s ',{'user_id': session['id'] })
            notes = cursor.fetchall()
            session.pop('notes', None)
            session['notes'] = notes
            flash('Note added!', category='success')
   

    return render_template("home.html" )

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from notes where id = %s',(noteId,))
    note = cursor.fetchone()
    print(note)
    if note:
        if note['user_id'] == session['id']:
            cursor.execute('delete from notes where id = %s', (note['id'],) )
            mysql.connection.commit()
            cursor.execute('SELECT * FROM notes WHERE user_id = %(user_id)s ',{'user_id': session['id'] })
            notes = cursor.fetchall()
            session.pop('notes', None)
            session['notes'] = notes
    return jsonify({})