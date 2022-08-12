from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app=Flask(__name__)

CORS(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# DB Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Note('{self.title}', {self.date_posted}', '{self.content}')"

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    notes =Note.query.all()
    # print(f"Notes: {notes}")
    return render_template("index.html", notes=notes)

@app.route("/add_note", methods=["POST"])
def add_note():
    title = request.form.get("title")
    content = request.form.get("content")
    
    note = Note(title=title, content=content)
    db.session.add(note)
    db.session.commit()
    
    return redirect(url_for("home"))


@app.route("/update/<int:note_id>", methods=["GET", "POST"])
def update_note(note_id):
    note = Note.query.filter_by(id=note_id).first()
    # db.session.commit()
    if request.method == "GET":
        # Get note by id
        # note = Note.query.filter_by(id=note_id).first()
        return render_template("update.html", note=note)
    elif request.method == "POST":
        # note.title = request.form.get("title")
        # note.content = request.form.get("content")
        print(note)
        
        note.title = request.form.get("title")
        note.content = request.form.get("content")
        
        print(note)
        
        db.session.commit()
        print(note.title)
        print(note.content)
        
        # note = Note(title=title, content=content)
        # db.session.add(note)
        flash('Your todo has been updated!', 'success')
        return redirect(url_for("home"))
    

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)