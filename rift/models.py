from flask import Flask
import datetime
from mongoengine import Document
from mongoengine.fields import \
	(DateTimeField, EmbeddedDocumentField, ListField, ReferenceField, StringField, EmailField)

# Models
class User(Document):
	firstName = StringField(required=True)
	lastName = StringField(required=True)
	username = StringField(required=True, unique=True)
	email = EmailField(unique=True)
	password = StringField(required=True)

class Post(Document):
	title = StringField(max_length=64, required=True)
	content = StringField(max_length=20000, required=True)
	author = ReferenceField(User)
	date = DateTimeField(default=datetime.datetime.utcnow)
	
	meta = {'allow_inheritance': True}

class WriteupCollection(Document):
	name = StringField(max_length=64, required=True)

class Writeup(Post):
	collection = ReferenceField(WriteupCollection)