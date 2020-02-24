from collections.abc import Mapping
#TODO: This is wonky. Look for a better way to store permissions structure.

class Permission:
	def __init__(self, tag, description):
		self.tag = tag
		self.description = description

class Role:
	__roles : dict = {}

	def __init__(self, name, permissions : set):
		self.name = name
		self.permissions = permissions
		self.__class__.__roles.update({name: self})
		print("[+] Loaded Permissions '" + name + "' Role. " + str(len(self.__class__.__roles)))

	def HasPermission(self, permission : Permission):
		if(permission in self.permissions or permission is None):
			return True
		else:
			return False

	@staticmethod
	def Get(roleName: str):
		try:
			return Role.__roles[roleName]
		except KeyError as e:
			print("[!] There is no role by the name of '" + roleName + "'. Returning guest role.")
			return Role("Guest", {})

	@staticmethod
	def List():
		return Role.__roles
		

# PERMISSIONS
CreateCTFs = Permission('CreateCTFs', "Allows the user to create, edit, and delete their own In-house CTFs, including challenges.")
ModerateCTFs = Permission('ModerateCTFs', "Allows the user to edit other's CTFs and challenges.")

EditUserRoles = Permission('EditUserRoles', "Allows the user to edit the permission roles of all non-admin users.")

# ROLES
Role("Guest", {})

Role("Member", {})

Role("Creator", {
	CreateCTFs
})

Role("Admin", {
	CreateCTFs,
	ModerateCTFs,
	EditUserRoles
})