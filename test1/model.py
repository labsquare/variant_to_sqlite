from peewee import * 

db = SqliteDatabase('variant.db')
class Variant(Model):
	chrom = CharField()
	pos   = IntegerField()
	ref   = CharField()
	alt   = CharField()
	class Meta:
		database = db 


db.connect()
db.create_tables([Variant], safe = True)
