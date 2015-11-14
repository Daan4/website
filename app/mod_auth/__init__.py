def setup_module(nav, nav_bar):
    nav_bar.items.append(nav.Item('Log in', 'auth.login', constraints=[nav.Item.REQUIRELOGOUT]))
    nav_bar.items.append(nav.Item('Log out', 'auth.logout', constraints=[nav.Item.REQUIRELOGIN]))
