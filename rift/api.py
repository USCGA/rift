from flask import Blueprint, request
import rift.models as models
import rift.user as user
import rift.permissions as permissions
import rift.uploads as uploads

# All routes defined below belong to the "apiRoutes" blueprint 
# which is applied to flask.app in __init__.py.
apiRoutes = Blueprint("page", __name__)

@apiRoutes.route("api/ctf", methods=['GET','POST'])
def api_ctf():
    if (request.method == 'GET'):
        pass
    if (request.method == 'POST'):
        pass

# EXCEPTIONS
class NotAuthorizedError(Exception):
    """Exception raised for API calls that are not authorized with provided credientials.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, message, details):
        self.message = message
        self.details = details

@staticmethod
def NewCTF(userDocument, ctfTitle, ctfDescription=""):
    if (user.HasPermission(userDocument)):
        newCTF = models.CTF()
        newCTF.name = ctfTitle
        newCTF.description = ctfDescription
        newCTF.author = userDocument
        newCTF.save()
    else:
        message = "User " + str(userDocument.id) + " does not have permission to create CTFs."
        details = "A user attempted to create a CTF without the appropriate permissions"
        raise NotAuthorizedError(message, details)