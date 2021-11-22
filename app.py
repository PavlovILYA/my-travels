from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    route = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Travel %r' % self.id


@app.route('/create-travel', methods=['POST', 'GET'])
def create_travel():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        route = request.form['route']
        description = request.form['description']
        status = request.form['status']

        travel = Travel(title=title, author=author, route=route, description=description, status=status)

        try:
            db.session.add(travel)
            db.session.commit()
            return redirect('/travels')
        except:
            return "Ошибка при добавлении путешествия"
    else:
        return render_template("create-travel.html")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/travels')
def all_travels():
    travels = Travel.query.order_by(Travel.date.desc()).all()
    return render_template("travels.html", travels=travels)


@app.route('/travels/<int:id>')
def detail(id):
    travel = Travel.query.get(id)
    return render_template("detail.html", travel=travel)


@app.route('/travels/<int:id>/delete')
def delete_travel(id):
    travel = Travel.query.get_or_404(id)

    try:
        db.session.delete(travel)
        db.session.commit()
        return redirect('/travels')
    except:
        "Ошибка при удалении путешествия"


@app.route('/travels/<int:id>/update', methods=['POST', 'GET'])
def update_travel(id):
    travel = Travel.query.get(id)
    if request.method == "POST":
        travel.title = request.form['title']
        travel.author = request.form['author']
        travel.route = request.form['route']
        travel.description = request.form['description']
        travel.status = request.form['status']

        try:
            db.session.commit()
            return redirect('/travels')
        except:
            return "Ошибка при редактировании путешествия"
    else:
        return render_template("update-travel.html", travel=travel)


if __name__ == "__main__":
    app.run(debug=False)
