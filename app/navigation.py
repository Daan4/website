from flask_navigation import Navigation
from flask_navigation.item import Item
from flask_navigation.utils import BoundTypeProperty


class NavBarItem(Item):
    """ Overrides flask_navigation.item.Item to add the show() function.
        show() is called to see if the Navigation Bar Item should be
        shown or not depending on constraints given to the Navigation Bar Item.
        Constraints
        REQUIRELOGIN: show the item only when the user is logged in
        REQUIRELOGIN: show the item only when the user is logged out
    """
    REQUIRELOGIN = 0
    REQUIRELOGOUT = 1

    def __init__(self, label, endpoint, args=None, url=None, html_attrs=None,
                 items=None, constraints=None):
        super().__init__(label, endpoint, args, url, html_attrs, items)
        self.constraints = constraints if constraints else []

    def show(self):
        from app.mod_auth.views import user_is_logged_in
        user_logged_in = user_is_logged_in()
        for constraint in self.constraints:
            if constraint == self.REQUIRELOGIN:
                if not user_logged_in:
                    break
            elif constraint == self.REQUIRELOGOUT:
                if user_logged_in:
                    break
        else:
            return True
        return False


class MyNavigation(Navigation):
    """ Overrides Flask-Navigation Navigation class to change
    Item class to NavBarItem instead of flask_navigation.item.Item
    """
    Item = BoundTypeProperty('Item', NavBarItem)

    def __init__(self, app=None):
        super().__init__(app)




# from flask import g
#
# CONSTRAINT_LOGIN = 0  # the user has to be logged in.
# CONSTRAINT_LOGOUT = 1  # the user has to be logged out.
#
#
# class Navigation:
#     def __init__(self, app, bars=None):
#         self.bars = bars if bars else {}
#
#         # Add this object to the context of all templates
#         # can be accessed via the variable nav
#         @app.context_processor
#         def inject_navigation():
#             return dict(nav=self)
#
#     def add_bar(self, bar):
#         self.bars[bar.name] = bar.items
#
#
# class Bar:
#     def __init__(self, name, items=None):
#         self.name = name
#         self.items = items if items else []
#
#     def add_item(self, item):
#         self.items.append(item)
#
#
# class Item:
#     def __init__(self, href, id, caption, *constraints):
#         self.href = href
#         self.id = id
#         self.caption = caption
#         self.constraints = constraints
#
#     def is_active(self):
#         active = True
#         for constraint in self.constraints:
#             if constraint == CONSTRAINT_LOGIN:
#                 if not(g.user is not None and g.user.is_authenticated):
#                     active = False
#             elif constraint == CONSTRAINT_LOGOUT:
#                 if g.user is not None and g.user.is_authenticated:
#                     active = False
#         return active
#
#
# def init_navigation(nav):
#     nav.add_bar(Bar('base', [
#         Item('/', 'index', 'Home'),
#         Item('/projects', 'projects', 'Projects'),
#         Item('/streams', 'streams', 'Streams'),
#         Item('/adminpanel', 'adminpanel', 'Admin Panel', CONSTRAINT_LOGIN),
#         Item('/login', 'login', 'Log in', CONSTRAINT_LOGOUT),
#         Item('/logout', 'logout', 'Log out', CONSTRAINT_LOGIN)
#     ]))
#
#     nav.add_bar(Bar('adminpanel', [
#         Item('/adminpanel/projects', 'projects', 'Projects'),
#         Item('/adminpanel/streams', 'streams', 'Streams')
#     ]))
