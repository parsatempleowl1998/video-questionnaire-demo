from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db, app
import json
import os
from werkzeug.utils import secure_filename
import urllib.request

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/list-of-us-airlines')
@login_required
def listOfUSAirlines():
    return render_template("list_of_us_airlines.html", user=current_user)

@views.route('/video-questionnaire')
@login_required
def video_upload_form():
    return render_template('upload_display_video.html', user=current_user)

@views.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        flash('No video file', category='error')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No video selected for uploading', category='error')
        return redirect(request.url)
    else:
        filename = secure_filename(file.filename)
        file=file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_video filename: ' + filename)
        flash('Video successfully uploaded and displayed below', category='success')
        #return render_template('upload_display_video.html', filename=filename)
        return redirect("http://videoqa.paris.inria.fr/vqa?video_id=weWB3weqau4", code=302)
    
@views.route('/display/<filename>')
def display_video(filename):
    return render_template('upload_display_video.html', )
    #print('display_video filename: ' + filename)
    #return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return redirect(url_for('./', filename=filename), code=301)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
