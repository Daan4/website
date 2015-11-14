from flask import Blueprint, render_template, flash
from app import db
from app.mod_projects.models import Project
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError
from .forms import ConfigForm

mod_projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')


@mod_projects.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    return render_template('projects.html', title="Projects", projects=projects)


# Used by mod_adminpanel module to do configuration form logic.
def do_config_form_logic(form):
    project_data = form.project.data
    content_data = form.content.data
    if form.add.data:
        project = Project(name=project_data, content=content_data)
        try:
            db.session.add(project)
            db.session.commit()
            flash('Project {} added'.format(project_data))
        except (IntegrityError, InvalidRequestError):
            flash('Project {} already exists in the database'.format(project_data))
    elif form.remove.data:
        project = Project.query.filter_by(name=project_data).first()
        try:
            db.session.delete(project)
            db.session.commit()
            flash('Project {} removed'.format(project_data))
        except UnmappedInstanceError:
            flash('Project {} doesn\'t exist in the database.'.format(project_data))
