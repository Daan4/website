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