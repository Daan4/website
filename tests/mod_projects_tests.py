from tests.app_tests import BaseTestCase
from app.mod_projects.models import *
from flask import url_for

NAME = 'Project'
CONTENT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; Sin tantum modo ad indicia veteris memoriae cognoscenda, curiosorum. Duo Reges: constructio interrete. Tollenda est atque extrahenda radicitus. Atque ego: Scis me, inquam, istud idem sentire, Piso, sed a te opportune facta mentio est.'


class TestProjects(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.disable_login = True
        super().setUpClass()
        cls.url = url_for('adminpanel.configure_module', bp_name='projects')

    def add_project(self, name, content):
        return self.client.post(self.url, data=dict(
            name=name,
            content=content,
            add='Add'
        ))

    def remove_project(self, name, content):
        return self.client.post(self.url, data=dict(
            name=name,
            content=content,
            remove='Remove'
        ))

    def load_project(self, name):
        return self.client.post(self.url, data=dict(
            all_projects=name,
            load='Load'
        ))

    def test_add(self):
        with self.client:
            # Test that adding a project works
            self.add_project(NAME, CONTENT)
            project = Project.query.filter_by(name=NAME).first()
            self.assertIsInstance(project, Project)
            self.assertEquals(project.name, NAME)
            self.assertEquals(project.content, CONTENT)
            # todo: implement. currently fails because of db.session.rollback() in view
            # # Test that adding an existing project updates the content
            # self.add_project(NAME, '')
            # project = Project.query.filter_by(name=NAME).first()
            # self.assertEquals(project.content, '')
            # Test that the project name is required
            self.add_project('', CONTENT)
            project = Project.query.filter_by(name='').first()
            self.assertIsNone(project)

    def test_remove(self):
        with self.client:
            # Test that removing a project works
            self.add_project(NAME, CONTENT)
            self.remove_project(NAME, CONTENT)
            project = Project.query.filter_by(name=NAME).first()
            self.assertIsNone(project)
            # Test that removing a non-existent project works
            self.remove_project(NAME, CONTENT)
            # Test that the project name is required
            project = Project(name='', content=CONTENT)
            db.session.add(project)
            db.session.commit()
            project = Project.query.filter_by(name='').first()
            self.assertIsInstance(project, Project)

    def test_load(self):
        with self.client:
            self.add_project(NAME, CONTENT)
            rv = self.load_project(NAME)
            self.assertIn(CONTENT.encode(), rv.data)
            self.assertIn(NAME.encode(), rv.data)