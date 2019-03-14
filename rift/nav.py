# Navigation Menus
# menu > category > section > subsection > item
# (Menus have categories have sections have subsections have items.)

# ----- MENU CLASSES -----

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


# ----- MENU ITEMS -----

# Guest Menu
item_home = MenuItem("Rift", "/dashboard")
item_github = MenuItem("GitHub", "http://www.github.com/USCGA")
item_public_bulletin = MenuItem("Bulletin", "#") # TODO: Implement public bulletin
item_team = MenuItem("Team", "#") # TODO: Implement public team page
item_contact = MenuItem("Contact", "#") # TODO: Implement public contact page

# Session Management
item_login = MenuItem("Login", "/login")
item_logout = MenuItem("Logout", "/logout")

# Play
item_scoreboard = MenuItem("Scoreboard", "/scoreboard")

# Dummy (Subsections can't be empty, so this is necessary during development)
item_dummy = MenuItem("item_dummy", "#")

# ----- MENU ITEM Collections ------
# (This is necessary for the landing pages at "/")
guest_menu = [item_home, item_github, item_public_bulletin, item_team, item_contact]

# ----- MENU SUBSECTIONS -----
subsection_login = MenuSubSection("Login / Logout", [item_login, item_logout])
subsection_latest = MenuSubSection("Latest",[item_dummy])
subsection_inhouse = MenuSubSection("In House", [item_scoreboard])
subsection_curated = MenuSubSection("Curated", [item_dummy])
subsection_skilltree = MenuSubSection("Skill Tree", [item_dummy])
subsection_announcements = MenuSubSection("Announcements", [item_dummy])
subsection_accountsettings = MenuSubSection("Account Settings", [item_dummy])

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