from flask import Flask
import datetime
from mongoengine import Document
from mongoengine.fields import \
	(DateTimeField, EmbeddedDocumentField, ListField, ReferenceField, StringField, EmailField)

# Models
class Motd(Document):
	title = StringField(max_length=200, required=True)
	message = StringField(max_length=500, required=True)
	date_created = DateTimeField(default=datetime.datetime.utcnow)

class User(Document):
	username = StringField(max_length=32, required=True, unique=True)
	email = EmailField(max_length=64, unique=True)
	password = StringField(required=True)