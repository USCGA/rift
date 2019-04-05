from flask import Flask
import datetime
from mongoengine import (Document, PULL, CASCADE)
from mongoengine.fields import \
	(DateTimeField, EmbeddedDocumentField, ListField, EmbeddedDocumentListField, ReferenceField, StringField, EmailField, URLField, ListField)

# Models
class User(Document):
	firstName = StringField(required=True)
	lastName = StringField(required=True)
	username = StringField(required=True, unique=True)
	email = EmailField(unique=True)
	password = StringField(required=True)

class Post(Document):
	title = StringField(max_length=64, required=True)
	content = StringField(max_length=50000, required=True)
	author = ReferenceField(User)
	date = DateTimeField(default=datetime.datetime.utcnow)
	meta = {'allow_inheritance': True}

class WriteupCollection(Document):
	name = StringField(max_length=64, unique=True, required=True)
	description = StringField(max_length=1000, required=True)
	year = StringField(max_length=12)
	link = URLField()

class Writeup(Post):
	category = StringField(max_length=16, required=True)
	collection = ReferenceField(WriteupCollection, reverse_delete_rule=CASCADE)

class Announcement(Post):
	pass