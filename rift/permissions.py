#TODO: This is wonky. Look for a better way to store permissions structure.

class Permission: 
    def __init__(self, tag, description):
        self.tag = tag
        self.description = description

# PERMISSIONS
CreateWriteups = Permission('CreateWriteups', "Allows the user to create, edit, and delete their own Writeups.")
ModerateWriteups = Permission('ModerateWriteups', "Allows the user to edit and delete other's Writeups.")

CreateCTFs = Permission('CreateCTFs', "Allows the user to create, edit, and delete their own In-house CTFs, including challenges.")
ModerateCTFs = Permission('ModerateCTFs', "Allows the user to edit other's CTFs and challenges.")

CreateAnnouncements = Permission('CreateAnnouncements', "Allows the user to create and edit their own Announcements.")
ModerateAnnouncements = Permission('ModerateAnnouncements', "Allows the user to edit and delete other's Announcements.")

EditUserRoles = Permission('EditUserRoles', "Allows the user to edit the permission roles of all non-admin users.")
# PERMISSION SETS

# Members can view all content and create writups.
Member = set([
    CreateWriteups.tag
    ])

# Architects are members with permission to make CTFs.
Architect = set([
    CreateCTFs.tag
    ]).union(Member)

# Deputies are members with permission to make CTFs and announcements.
Deputy = set([
    CreateAnnouncements.tag
    ]).union(Architect)

# Team Captains can moderate (edit/remove) all user-generated content.
# They may also make announcements and CTFs.
Captain = set([
    ModerateWriteups.tag,
    ModerateCTFs.tag,
    ModerateAnnouncements.tag,
    EditUserRoles.tag
    ]).union(Deputy)

# This role is reserved for individuals maintaining the application and
# should have all permissions.
Admin = set().union(Captain)

# This is allows permission sets to be accessed by role name.
Roles = {
    "Admin": Admin,
    "Captain": Captain,
    "Deputy": Deputy,
    "Architect": Architect,
    "Member": Member
}