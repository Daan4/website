class Navigation():
    def __init__(self, app, bars=None):
        self.bars = bars if bars else {}

        # Add this object to the context of all templates
        # can be accessed via the variable nav
        @app.context_processor
        def inject_navigation():
            return dict(nav=self)

    def add_bar(self, bar):
        self.bars[bar.name] = bar.items


class Bar():
    def __init__(self, name, items=None):
        self.name = name
        self.items = items if items else []


class Item():
    def __init__(self, href, caption):
        self.href = href
        self.caption = caption


def init_navigation(nav):
    nav.add_bar(Bar('base', [Item('/index', 'Home'),
                             Item('https://www.github.com/ziel980', 'GitHub'),
                             Item('/projects', 'Projects'),
                             Item('/streams', 'Streams'),
                             Item('/configuration', 'Configuration'),
                             Item('/login', 'Log in'),
                             Item('/logout', 'Log out')
                             ]))