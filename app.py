from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create the extension
db = SQLAlchemy()
# initialize the app with the extension
db.init_app(app)


class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),  nullable=False)
    description = db.Column(db.String(500),  nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} :- {self.title}"

# creating database
with app.app_context():
    db.create_all()

@app.route("/", methods = ["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        titl = request.form['title']
        descr = request.form['description']
        todo = Todo(title=titl, description=descr)
        # Inserts records into a mapping table
        db.session.add(todo)
        db.session.commit()

    # retrieves all records (corresponding to SELECT queries) from the table.
    todos = Todo.query.all()    
    return render_template("index.html", mytodo = todos)


@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    if request.method == 'POST':
        titl = request.form['title']
        descr = request.form['description']
        todo = Todo.query.filter_by(Sno = sno).first()
        todo.title = titl
        todo.description = descr
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(Sno = sno).first()
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(Sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)