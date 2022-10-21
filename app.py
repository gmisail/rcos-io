from flask import Flask
from flask import render_template

import db

app = Flask(__name__)

@app.route('/')
def index():
    return "<p>hello world</p>"

@app.route('/projects')
def projects():
    projects = db.get_semester_projects("202201", False)
    return render_template("projects.html", projects=projects)

@app.route('/project/<project_id>')
def project(project_id): 
    project = db.get_project(project_id)

    print(project)

    if len(project) == 1:
        project = project[0]

    return render_template("project.html", project=project)
