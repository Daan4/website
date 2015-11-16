from flask import render_template, flash, Blueprint
from app import db
from .models import Project
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError
from .forms import EditProjectForm
from app.mod_adminpanel.views import register_adminpanel

mod_projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates',
                         static_folder='static')


@mod_projects.route('/', methods=['GET'])
def index():
    projects = Project.query.all()
    return render_template('projects.html', title="Projects", projects=projects)


# Used by mod_adminpanel module to do configuration form logic.
@register_adminpanel(mod_projects.name)
def do_adminpanel_logic():
    edit_form = EditProjectForm()
    # Drop down list shows all projects.
    all_projects = Project.query.all()
    edit_form.all_projects.choices = [(p.name, p.name) for p in all_projects]
    # Determine what button was pressed and act acccordingly.
    if edit_form.validate_on_submit():
        name = edit_form.name.data
        content = edit_form.content.data
        selected_project = edit_form.all_projects.data
        if edit_form.add.data:
            add_project(name, content, edit_form)
        elif edit_form.remove.data:
            delete_project(name, edit_form)
        elif edit_form.load.data:
            load_project(selected_project, edit_form)
    return render_template('projects_config.html', edit_form=edit_form, title='Admin Panel - Projects')


def add_project(name, content, form):
    project = Project(name=name, content=content)
    try:
        db.session.add(project)
        db.session.commit()
        form.all_projects.choices.append((project.name, project.name))
        flash('Project {} added'.format(name))
    except (IntegrityError, InvalidRequestError):
        # A project with this name already exists, update its content instead.
        db.session.rollback()
        project = Project.query.filter_by(name=name).first()
        try:
            db.session.add(project)
            db.session.commit()
            flash('Project {} content updated'.format(name))
        except Exception as e:
            # todo: which exceptions can occur?
            db.session.rollback()
            raise e


def delete_project(name, form):
    project = Project.query.filter_by(name=name).first()
    try:
        db.session.delete(project)
        db.session.commit()
        form.all_projects.choices.remove((project.name, project.name))
        flash('Project {} removed'.format(name))
    except UnmappedInstanceError:
        db.session.rollback()
        flash('Project {} doesn\'t exist in the database'.format(name))


def load_project(name, form):
    project = Project.query.filter_by(name=name).first()
    if project:
        form.name.data = project.name
        form.content.data = project.content
        for i, choice in enumerate(form.all_projects.choices):
            if choice[0] == name:
                form.all_projects = i
        flash('Project {} loaded'.format(name))
    else:
        flash('Project {} doesn\'t exist in the database'.format(name))
