from flask import Flask
import datetime
from mongoengine import (Document, PULL, CASCADE)
from mongoengine.fields import \
	(DateTimeField, EmbeddedDocumentField, IntField, ListField, EmbeddedDocumentListField, ReferenceField, GenericReferenceField, StringField, EmailField, URLField, ListField)

# Models
class User(Document):
	firstName = StringField(required=True)
	lastName = StringField(required=True)
	username = StringField(required=True, unique=True)
	email = EmailField(unique=True)
	password = StringField(required=True)
	score = IntField(default=0)
	completed_challenges = ListField(ReferenceField('CTFChallenge'), reverse_delete_rule=PULL)

class Post(Document):
	title = StringField(max_length=64, required=True)
	content = StringField(max_length=50000, required=True)
	author = ReferenceField('User')
	date = DateTimeField(default=datetime.datetime.utcnow)
	meta = {'allow_inheritance': True}

class WriteupCollection(Document):
	name = StringField(max_length=64, unique=True, required=True)
	description = StringField(max_length=1000, required=True)
	year = StringField(max_length=12)
	link = URLField()

class Writeup(Post):
	category = StringField(max_length=32, required=True)
	collection = ReferenceField('WriteupCollection', reverse_delete_rule=CASCADE)

class Announcement(Post):
	pass

class CTF(Document):
	name = StringField(max_length=64, unique=True, required=True)
	description = StringField(max_length=1000, required=True)
	author = ReferenceField('User')

class CTFChallenge(Document):
	title = StringField(max_length=64, required=True)
	description = StringField(max_length=50000, required=True)
	category = StringField(max_length=32, required=True)
	point_value = IntField(0,10000, default=0)
	filename = StringField()
	flag = StringField(max_length=128)
	author = ReferenceField('User')
	ctf = ReferenceField(CTF, reverse_delete_rule=CASCADE)
	docker_cid = StringField(max_length=32)
	date = DateTimeField(default=datetime.datetime.utcnow)
	