from flask import current_app, url_for
# Navigation Menus
# menu > category > section > subsection > item
# (Menus have categories have sections have subsections have items.)

# ----- MENU CLASSES -----

class MenuItem:
	def __init__(self, name, target, *, is_url=False, **kwargs):
		"""Defines name and page for each menu item."""
		self.name = name
		self.__target = target
		self.is_url = is_url
		self.__kwargs = kwargs

	# This function is kind of a hack. It allows url_for to be computed during a request.
	# Without doing that, url_for would fail in predefined MenuItem instances because this 
	# file is imported before the Flask app initializes and creates the application context.
	#
	# This is nice though because both external urls (eg. item_github) and dynamically referenced
	# internal pages (eg. item_dashboard) can use this single class.
	#
	# However, I imagine doing this operation for every menu_item on every request is
	# a waste of computation. I'll find a better way to do this later. TODO Optimize rift.nav
	@property
	def url(self):
		if (self.is_url == True):
			# If the target is already a url, return it.
			return self.__target
		else:
			# If the target is a page reference (eg. 'page.home'),
			# resolve the url and return that instead.
			if self.__kwargs is None:
				return url_for(self.__target)
			else:
				# If there are additional kwargs, return the url with those arguments.
				return url_for(self.__target, **self.__kwargs)

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
item_home = MenuItem("Rift", "page.dashboard")
item_github = MenuItem("GitHub", "http://www.github.com/USCGA", is_url=True)
item_publicbulletin = MenuItem("Bulletin", "#", is_url=True) # TODO Implement public bulletin
item_team = MenuItem("Team", "#", is_url=True) # TODO Implement public team page
item_contact = MenuItem("Contact", "#", is_url=True) # TODO Implement public contact page

# Learn
item_writeups = MenuItem("Writeups", 'page.writeups')
item_writeup_collections = MenuItem("Collections", 'page.writeup_collections')
item_new_writeup = MenuItem("New Writeup", "page.new_writeup")

# Options
item_login = MenuItem("Login", "page.login")
item_logout = MenuItem("Logout", "page.logout")
item_profile = MenuItem("Profile", "page.profile")

# Posts
item_announcements = MenuItem("Announcements", "page.posts", type="Announcement")
item_new_announcement = MenuItem("New Announcement", "page.new_announcement")

# Play
item_scoreboard = MenuItem("Scoreboard", "#", is_url=True)

# Dummy (Subsections can't be empty, so this is necessary during development)
item_dummy = MenuItem("item_dummy", "#", is_url=True)

# ----- MENU ITEM Collections ------
# (This is necessary for the landing pages at "/")
guest_menu = [item_home, item_github, item_publicbulletin, item_team, item_contact]

# ----- MENU SUBSECTIONS -----
subsection_login = MenuSubSection("Login / Logout", [item_login, item_logout])
subsection_latest = MenuSubSection("Latest",[item_dummy])
subsection_inhouse = MenuSubSection("In House", [item_scoreboard])
subsection_curated = MenuSubSection("Curated", [item_dummy])
subsection_skilltree = MenuSubSection("Skill Tree", [item_dummy])
subsection_read = MenuSubSection("Read", [item_announcements])
subsection_write = MenuSubSection("Write", [item_new_announcement])
subsection_writups = MenuSubSection("Read", [item_writeups, item_writeup_collections, item_new_writeup])
subsection_accountsettings = MenuSubSection("Account Settings", [item_profile])

# ----- MENU SECTIONS -----
section_posts = MenuSection("Posts", "section_posts", "fa-comments", [subsection_read, subsection_write])
section_ctf = MenuSection("CTF", "section_ctf", "fa-flag-checkered", [subsection_latest, subsection_inhouse, subsection_curated])
section_skills = MenuSection("Skills", "section_skills", "fa-flask", [subsection_skilltree])
section_writeups = MenuSection("Writeups", "section_writeups", "fa-book", [subsection_writups])
section_account = MenuSection("Account", "section_account", "fa-address-card", [subsection_accountsettings, subsection_login])

# ----- MENU CATEGORY -----
category_bulletin = MenuCategory("Bulletin", [section_posts])
category_play = MenuCategory("Play", [section_ctf])
category_learn = MenuCategory("Learn", [section_skills, section_writeups])
category_options = MenuCategory("Options", [section_account])

# ----- MENUS -----
menu_main = Menu([category_bulletin, category_play, category_learn, category_options])