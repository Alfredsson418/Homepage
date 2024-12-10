from flask import Flask, render_template, request, url_for
import logs.log as log
import db.db as db
from db.db import blog_class, project_class

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

database = db.db("db/database.db");

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    projects = database.get_table(project_class())
    return render_template("projects.html", projects=projects)

@app.route("/blog")
def blog():
    blog = database.get_table(blog_class())
    return render_template("blog.html", blog=blog)

@app.route("/socials")
def socials():
    return render_template("socials.html")

@app.route("/modify/projects", methods=('GET', 'POST'))
def modify_project():
    if request.method == 'POST':
        action = request.form['action']
        if action == "delete":
            project = project_class()
            project.id = request.form['id']
            database.delete(project)

        elif action == "create":
            new_project = project_class()
            new_project.name = request.form['name']
            new_project.url = request.form['url']
            new_project.color = request.form['color']
            new_project.descr = request.form['descr']
            database.set_new(new_project)

        elif action == "modify":
            modify_project = project_class()
            modify_project.id = request.form['id']
            modify_project.id_old = request.form['id_old']
            modify_project.name = request.form['name']
            modify_project.url = request.form['url']
            modify_project.color = request.form['color']
            modify_project.descr = request.form['descr']
            database.update(modify_project)

    projects = database.get_table(project_class())
    return render_template("modify_project.html", projects=projects)

@app.route("/modify/blog", methods=('GET', 'POST'))
def modify_blog():
    if request.method == 'POST':
        action = request.form['action']
        if action == "delete":
            post = blog_class()
            post.id = request.form['id']
            database.delete(post)

        elif action == "create":
            new_post = blog_class()
            new_post.title = request.form['title']
            new_post.text = request.form['text']
            database.set_new(new_post)

        elif action == "modify":
            modify_post = blog_class()
            modify_post.id = request.form['id']
            modify_post.title = request.form['title']
            modify_post.text = request.form['text']
            database.update(modify_post)

    blog = database.get_table(blog_class())
    return render_template("modify_blog_posts.html", blog=blog)


if __name__ == "__main__":
   	app.run(debug=True, host="0.0.0.0")
