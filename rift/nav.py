from flask import current_app, url_for
import rift.permissions as permissions
# Navigation Menus
# menu > category > section > subsection > item
# (Menus have categories have sections have subsections have items.)

# ----- MENU CLASSES -----

class MenuItem:
	def __init__(self, name, target, *, is_url=False, permission=None, **kwargs):
		"""Defines name and page for each menu item."""
		self.name = name
		self.__target = target
		self.is_url = is_url
		self.permission = permission
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
	def __init__(self, name, items, permission=None):
		"""Menu items are sorted into sections"""
		self.name = name
		self.items = items

class MenuSection:
	def __init__(self, name, id, fa_icon, subsections, permission=None):
		"""Menu items are sorted into sections"""
		self.name = name
		self.id = id # Used for template targetdata
		self.fa_icon = fa_icon
		self.subsections = subsections

class MenuCategory:
	def __init__(self, name, sections, permission=None):
		"""Menu sections are sorted into menu categories"""
		self.name = name
		self.sections = sections

class Menu:
	def __init__(self, categories, permission=None):
		"""Menu categories are sorted into menus"""
		self.categories = categories


# ----- MENU ITEMS -----
# Guest Menu
item_home = MenuItem("Rift", "page.dashboard")
item_github = MenuItem("GitHub", "http://www.github.com/USCGA", is_url=True)
#item_publicbulletin = MenuItem("Bulletin", "#", is_url=True) # TODO Implement public bulletin
#item_team = MenuItem("Team", "#", is_url=True) # TODO Implement public team page
#item_contact = MenuItem("Contact", "#", is_url=True) # TODO Implement public contact page

# Bulletin
item_announcements = MenuItem("Announcements", "page.posts", type="Announcement")
item_new_announcement = MenuItem("New Announcement", "page.new_announcement")

# Play
item_homebrew_collections = MenuItem("Homebrew CTFs", 'page.ctfs')
item_scoreboard = MenuItem("Scoreboard", "page.scoreboard")

# Learn
item_writeups = MenuItem("Writeups", 'page.writeups')
item_writeup_collections = MenuItem("Collections", 'page.collections')
item_new_writeup = MenuItem("New Writeup", "page.new_writeup")

# Options
item_login = MenuItem("Login", "page.login")
item_logout = MenuItem("Logout", "page.logout")
item_profile = MenuItem("Profile", "page.profile")

# Admin
item_rift_status = MenuItem("Status", "page.rift_status")
item_rift_users = MenuItem("User Management", "page.rift_users")

# Dummy (Subsections can't be empty, so this is necessary during development)
item_dummy = MenuItem("Not implemented", "#", is_url=True)

# ----- MENU ITEM Collections ------
# (This is necessary for the landing pages at "/")
guest_menu = [item_home, item_github]

# ----- MENU SUBSECTIONS -----
subsection_login = MenuSubSection("Login / Logout", [item_login, item_logout])
subsection_inhouse = MenuSubSection("In House", [item_homebrew_collections, item_scoreboard])
subsection_accountsettings = MenuSubSection("Account Settings", [item_profile])
subsection_rift_management = MenuSubSection("Management", [item_rift_status, item_rift_users])

# ----- MENU SECTIONS -----
section_ctf = MenuSection("CTF", "section_ctf", "fa-flag-checkered", [subsection_inhouse])
section_account = MenuSection("Account", "section_account", "fa-address-card", [subsection_accountsettings, subsection_login])
section_rift = MenuSection("Rift", "section_rift", "fa-tools",[subsection_rift_management])

# ----- MENU CATEGORY -----
category_play = MenuCategory("Play", [section_ctf])
category_options = MenuCategory("Options", [section_account, section_rift])

# ----- MENUS -----
menu_main = Menu([category_play, category_options])

### FUNCTIONS
# UNTESTED
def GetMenuByRole(self, roleName : str):
	menu = menu_main
	role = permissions.Role.Get(roleName)

	for category in menu.categories:
		for section in category.sections:
			for subsection in section.subsections:
				for item in subsection.items:
					if not role.HasPermission(item.permission):
						subsection.items.remove(item)
				if len(subsection.items) == 0:
					section.subsections.remove(subsection)
			if len(section.subsections) == 0:
				category.sections.remove(section)
		if len(category.sections) == 0:
			menu.categories.remove(category)
	return menu