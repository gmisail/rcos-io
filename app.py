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

'''
    Render the projects page given a list of projects.
'''
def render_projects(projects):
    return render_template("projects.html", projects=projects)

'''
    Get all projects for a specific semester.
'''
@app.route("/projects/<semester>")
def semester_projects(semester=None):  
    if semester == None:
        return render_projects([], False)
    
    return render_projects(db.get_semester_projects(semester, False))

'''
    Get all projects for the current semester.
'''
@app.route("/projects")
def current_projects():
    return render_projects(db.get_semester_projects(get_current_semester(), False))

'''
    Get all projects for all past semesters, current semester included.
'''
@app.route("/projects/past")
def past_projects():
    return render_projects(db.get_all_projects())

@app.route("/project/<project_id>")
def project(project_id):
    project = db.get_project(project_id)

    if len(project) == 1:
        project = project[0]
    
    # get all semesters where the project had members
    semesters = set([ user['semester']['title'] for user in project['enrollments'] ])
    members_by_semester = {}

    for s in semesters:
        members_by_semester[s] = []

    for user in project['enrollments']:
        members_by_semester.get(user['semester']['title']).append(user)
        
    project['assignments'] = members_by_semester

    return render_template("project.html", project=project)
