from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "arunisto"
db.init_app(app)

#db creation
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

with app.app_context():
    db.create_all()
@app.route("/")
def index():
    try:
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        return render_template("index.html", users=users)
    except:
        flash("Some Error Occured")
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def user_create():
    if request.method == "POST":
            username = request.form["username"]
            email=request.form["email"]
            user = User(username=username, email=email,)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("Duplicate Value")
    return redirect(url_for('index'))

@app.route("/<int:id>/delete", methods=["GET"])
def user_delete(id):
    user = db.get_or_404(User, id)
    print("before : ",user)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)