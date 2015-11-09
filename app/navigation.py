from flask import g

CONSTRAINT_LOGIN = 0  # the user has to be logged in.
CONSTRAINT_LOGOUT = 1  # the user has to be logged out.


class Navigation:
    def __init__(self, app, bars=None):
        self.bars = bars if bars else {}

        # Add this object to the context of all templates
        # can be accessed via the variable nav
        @app.context_processor
        def inject_navigation():
            return dict(nav=self)

    def add_bar(self, bar):
        self.bars[bar.name] = bar.items


class Bar:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items if items else []


class Item:
    def __init__(self, href, id, caption, *constraints):
        self.href = href
        self.id = id
        self.caption = caption
        self.constraints = constraints

    def is_active(self):
        active = True
        for constraint in self.constraints:
            if constraint == CONSTRAINT_LOGIN:
                if not(g.user is not None and g.user.is_authenticated):
                    active = False
            elif constraint == CONSTRAINT_LOGOUT:
                if g.user is not None and g.user.is_authenticated:
                    active = False
        return active


def init_navigation(nav):
    nav.add_bar(Bar('base', [
        Item('/', 'index', 'Home'),
        Item('/projects', 'projects', 'Projects'),
        Item('/streams', 'streams', 'Streams'),
        Item('/adminpanel', 'adminpanel', 'Admin Panel', CONSTRAINT_LOGIN),
        Item('/login', 'login', 'Log in', CONSTRAINT_LOGOUT),
        Item('/logout', 'logout', 'Log out', CONSTRAINT_LOGIN)
    ]))
