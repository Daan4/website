from tests.app_tests import BaseTestCase
from app.mod_projects.models import *
from flask import url_for

NAME = 'Project'
CONTENT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; Sin tantum modo ad indicia veteris memoriae cognoscenda, curiosorum. Duo Reges: constructio interrete. Tollenda est atque extrahenda radicitus. Atque ego: Scis me, inquam, istud idem sentire, Piso, sed a te opportune facta mentio est.'


class TestProjects(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(disable_login=True)

    def post_config_form(self, data):
        return self.client.post(url_for('adminpanel.configure_module', bp_name='projects'), data=data)

    def create_test_project(self):
        db.session.add(Project(name=NAME, content=CONTENT))
        db.session.commit()

    def test_add(self):
        with self.client:
            self.post_config_form(dict(name=NAME,
                                       content=CONTENT,
                                       add='Add'))
            project = Project.query.filter_by(name=NAME).first()
            self.assertIsInstance(project, Project)
            self.assertEquals(project.name, NAME)
            self.assertEquals(project.content, CONTENT)

    def test_remove(self):
        with self.client:
            self.create_test_project()
            self.post_config_form(dict(name=NAME,
                                       content=CONTENT,
                                       remove='Remove'))
            project = Project.query.filter_by(name=NAME).first()
            self.assertIsNone(project)

    def test_load(self):
        with self.client:
            self.create_test_project()
            rv = self.post_config_form(dict(all_projects=NAME,
                                            load='Load'))
            self.assertTrue(CONTENT.encode() in rv.data)
