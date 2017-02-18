import os
from peewee import * 

try:
	os.remove("variant.db")
except : 
	pass
db = SqliteDatabase('variant.db')
class Variant(Model):
	chrom = CharField()
	pos   = IntegerField()
	ref   = CharField()
	alt   = CharField()
	class Meta:
		database = db 

class Field(Model):
	colname = CharField()
	desc    = CharField()
	class Meta:
		database = db

class Annotation(Model):
	variant = ForeignKeyField(Variant, related_name='variant')
	class Meta:
		database = db


db.connect()
db.create_tables([Variant, Field], safe = True)
