from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sn} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route("/delete/<int:sn>")
def delete(sn):
    todo_del = ToDo.query.filter_by(sn=sn).first()
    db.session.delete(todo_del)
    db.session.commit()
    return redirect("/")


@app.route("/edit/<int:sn>", methods=['GET', 'POST'])
def edit(sn):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sn=sn).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = ToDo.query.filter_by(sn=sn).first()
    return render_template('edit.html', todo=todo)


@app.route("/about")
def about():
    return "<h1>This Page is Under Development, Coming Soon...</h1>"


if __name__ == '__main__':
    app.run(debug=True)

