from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.mod_projects.models import Project

mod_projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')


@mod_projects.route('/', methods=['GET'])
def index():
    return render_template('projects.html', title="Projects")