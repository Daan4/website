from flask import Blueprint, request, render_template, flash, g,\
    session, redirect, url_for
from flask_login import login_required
from app import db
from app.mod_projects.models import Project
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError

mod_projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')


@mod_projects.route('/', methods=['GET'])
def index():
    return render_template('projects.html', title="Projects")


# Used by mod_adminpanel module to do configuration form logic.
def do_config_logic(form):
    project_data = form.project.data
    content_data = form.project_content.data
    if form.add.data:
        project = Project(name=project_data, content=content_data)
        try:
            db.session.add(project)
            db.session.commit()
            flash('Project {} added'.format(project_data))
        except (IntegrityError, InvalidRequestError):
            flash('Project {} already exists in the database'.format(project_data))
    elif form.remove.data:
        project = Project.query.filter_by(project=project_data).first()
        try:
            db.session.delete(project)
            db.session.commit()
            flash('Project {} removed'.format(project_data))
        except UnmappedInstanceError:
            flash('Project {} doesn\'t exist in the database.'.format(project_data))
