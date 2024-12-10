from flask import Flask, render_template, request, url_for
import logs.log as log
import db.db as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

database = db.db("db/database.db");

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    projects = database.get_table(db.project)
    return render_template("projects.html", projects=projects)

@app.route("/socials")
def socials():
    return render_template("socials.html")

@app.route("/create-project", methods=('GET', 'POST'))
def create_project():
    if request.method == 'POST':
        new_project = db.project
        new_project.name = request.form['name']
        new_project.name = request.form['url']
        database.set_new(new_project)
    return render_template("create_project.html")


if __name__ == "__main__":
   	app.run(debug=True, host="0.0.0.0")
