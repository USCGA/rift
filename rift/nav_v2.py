from flask import current_app, url_for
import rift.permissions as permissions
# Navigation Menus
# menu > category > section > subsection > item
# (Menus have categories have sections have subsections have items.)

full_menu = \
{
	"Play": \
		{
			"CTF": \
				{
					"__fa-icon": "fa-flag-checkered",
					"__sect-id": "section_ctf",
					"In-House": \
						{
							"Homebrew CTFs": "page.ctfs",
							"Scoreboard": "page.scoreboard"
						}
				}
		},
	"Options": \
		{
			"Account": \
				{
					"__fa-icon": "fa-address-card",
					"__sect-id": "section_account",
					"Account Settings": \
						{
							"Profile": "page.profile"
						},
					"Login / Logout": \
						{
							"Login": "page.login",
							"Logout": "page.logout"
						}
				},
			"Rift": \
				{
					"__fa-icon": "fa-tools",
					"__sect-id": "section_rift",
					"Management": \
						{
							"Status": "page.rift_status",
							"User Management": "page.rift_users"
						}
				}
		}
}

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

