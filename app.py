from flask import Flask, request, render_template
from datetime import date

import db

app = Flask(__name__)

def get_current_semester():
    current_date = date.today()
    start_month = "01"
    
    if current_date.month >= 5 and \
        current_date.month < 8:
        start_month = "05"
    elif current_date.month >= 8:
        start_month = "08"

    return "%d%s" % (current_date.year, start_month)

@app.route("/")
def index():
    return "<p>hello world</p>"

@app.route("/projects")
@app.route("/projects/<semester>")
def projects(semester=None):
    semester = get_current_semester() if semester is None else semester
     
    projects = db.get_semester_projects(semester, False)
    return render_template("projects.html", projects=projects)


@app.route("/project/<project_id>")
def project(project_id):
    project = db.get_project(project_id)

    if len(project) == 1:
        project = project[0]

    return render_template("project.html", project=project)
