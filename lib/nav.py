# Navigation Menus

class MenuItem:
	def __init__(self, name, url):
		"""Return a Customer object whose name is *name* and starting
		balance is *balance*."""
		self.name = name
		self.url = url

Home = MenuItem("Home", "/")
Login = MenuItem("Login", "/login")

items = [Home, Login]
