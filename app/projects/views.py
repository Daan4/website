from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.projects.models import Project

projects = Blueprint('projects', __name__, url_prefix='/projects')


@projects.route('/', methods=['GET'])
def index():
    return render_template('projects/projects.html')