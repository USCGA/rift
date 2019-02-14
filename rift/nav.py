# Navigation Menus

class MenuItem:
	def __init__(self, name, url):
		"""Return a Customer object whose name is *name* and starting
		balance is *balance*."""
		self.name = name
		self.url = url

# Default Menu
Home = MenuItem("Home", "/")
Learn = MenuItem("Learn", "#") # Unimplemented
Play = MenuItem("Play", "#") # Unimplemented
Team = MenuItem("Team", "#") # Unimplemented
Contact = MenuItem("Contact", "#") # Unimplemented

# Admin
Admin = MenuItem("Admin", "#") # Unimplemented

# Session Management
Login = MenuItem("Login", "/login")
Logout = MenuItem("Logout", "/logout")


# ----- MENUS ------
default_menu = [Home, Learn, Play, Team, Contact]
admin_menu = default_menu + [Admin]