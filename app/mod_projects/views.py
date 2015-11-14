from flask import Blueprint, render_template, flash
from app import db
from app.mod_projects.models import Project
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError
from .forms import ConfigForm, LoadProjectForm
from app.mod_adminpanel.views import register_adminpanel

mod_projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')


@mod_projects.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    return render_template('projects.html', title="Projects", projects=projects)


# Used by mod_adminpanel module to do configuration form logic.
@register_adminpanel(mod_projects.name)
def do_adminpanel_logic():
    config_form = ConfigForm()
    if config_form.validate_on_submit():
        name_data = config_form.name.data
        content_data = config_form.content.data
        if config_form.add.data:
            project = Project(name=name_data, content=content_data)
            try:
                db.session.add(project)
                db.session.commit()
                flash('Project {} added'.format(name_data))
            except (IntegrityError, InvalidRequestError):
                flash('Project {} already exists in the database'.format(name_data))
        elif config_form.remove.data:
            project = Project.query.filter_by(name=name_data).first()
            try:
                db.session.delete(project)
                db.session.commit()
                flash('Project {} removed'.format(name_data))
            except UnmappedInstanceError:
                flash('Project {} doesn\'t exist in the database.'.format(name_data))
        elif config_form.edit.data:
            pass

    load_form = LoadProjectForm()
    if load_form.validate_on_submit():
        pass
    all_projects = Project.query.all()
    load_form.projects.choices = [(p.name, p.name) for p in all_projects]
    return render_template('projects_config.html', config_form=config_form, load_form=load_form)
