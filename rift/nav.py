# Navigation Menus
# menu > category > section > subsection > item


class MenuItem:
	def __init__(self, name, url):
		"""Defines name and url for each menu item."""
		self.name = name
		self.url = url

class MenuSubSection:
	def __init__(self, name, items):
		"""Menu items are sorted into sections"""
		self.name = name
		self.items = items

class MenuSection:
	def __init__(self, name, id, subsections):
		"""Menu items are sorted into sections"""
		self.name = name
		self.id = id # Used for template targetdata
		self.subsections = subsections

class MenuCategory:
	def __init__(self, name, sections):
		"""Menu sections are sorted into menu categories"""
		self.name = name
		self.sections = sections

class Menu:
	def __init__(self, categories):
		"""Menu categories are sorted into menus"""
		self.categories = categories


# Default Menu
Home = MenuItem("Home", "/")
Learn = MenuItem("Learn", "/control")
Play = MenuItem("Play", "#") # Unimplemented
Team = MenuItem("Team", "#") # Unimplemented
Contact = MenuItem("Contact", "#") # Unimplemented

# Admin
Admin = MenuItem("Admin", "#") # Unimplemented

# Session Management
Login = MenuItem("Login", "/login")
Logout = MenuItem("Logout", "/logout")

# ----- MENU ITEM Collections ------
default_menu = [Home, Learn, Play, Team, Contact]
admin_menu = default_menu + [Admin]


## NEW TEMPLATE STUFF

# ----- MENU SUBSECTIONS -----
subsection_login = MenuSubSection("Login / Logout", [Login, Logout])

# ----- MENU SECTIONS -----
section_session = MenuSection("Session", "section_session", [subsection_login])

# ----- MENU CATEGORY -----
category_options = MenuCategory("Options", [section_session])

# ----- MENUS -----
menu_main = Menu([category_options])