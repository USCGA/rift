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
	def __init__(self, name, id, fa_icon, subsections):
		"""Menu items are sorted into sections"""
		self.name = name
		self.id = id # Used for template targetdata
		self.fa_icon = fa_icon
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
Home = MenuItem("Home", "/dashboard")
Learn = MenuItem("Learn", "/dashboard")
Play = MenuItem("Play", "/dashboard") # Unimplemented
Team = MenuItem("Team", "/dashboard") # Unimplemented
Contact = MenuItem("Contact", "/dashboard") # Unimplemented

# Admin
Admin = MenuItem("Admin", "#") # Unimplemented

# Session Management
Login = MenuItem("Login", "/login")
Logout = MenuItem("Logout", "/logout")

# Dummy
Dummy = MenuItem("MenuItem", "#")

# ----- MENU ITEM Collections ------
default_menu = [Home, Learn, Play, Team, Contact]
admin_menu = default_menu + [Admin]


## NEW TEMPLATE STUFF

# ----- MENU SUBSECTIONS -----
subsection_login = MenuSubSection("Login / Logout", [Login, Logout])
subsection_latest = MenuSubSection("Latest",[Dummy])
subsection_inhouse = MenuSubSection("In House", [Dummy])
subsection_curated = MenuSubSection("Curated", [Dummy])
subsection_skilltree = MenuSubSection("Skill Tree", [Dummy])
subsection_announcements = MenuSubSection("Announcements", [Dummy])
subsection_accountsettings = MenuSubSection("Account Settings", [Dummy])

# ----- MENU SECTIONS -----
section_posts = MenuSection("Posts", "section_posts", "fa-comments", [subsection_announcements])
section_ctf = MenuSection("CTF", "section_ctf", "fa-flag-checkered", [subsection_latest, subsection_inhouse, subsection_curated])
section_skills = MenuSection("Skills", "section_skills", "fa-flask", [subsection_skilltree])
section_account = MenuSection("Account", "section_account", "fa-address-card", [subsection_accountsettings, subsection_login])

# ----- MENU CATEGORY -----
category_bulletin = MenuCategory("Bulletin", [section_posts])
category_play = MenuCategory("Play", [section_ctf])
category_learn = MenuCategory("Learn", [section_skills])
category_options = MenuCategory("Options", [section_account])

# ----- MENUS -----
menu_main = Menu([category_bulletin, category_play, category_learn, category_options])