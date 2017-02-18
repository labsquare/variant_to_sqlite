#!/usr/bin/env python

# std
import re

# vcf
import vcf

# databasef
from peewee import *

# cli
import begin

db = SqliteDatabase("test.sqlite")

class Variant(Model):

    chrom = CharField()
    pos = CharField()
    ref = CharField()
    alt = CharField()

    class Meta:
        database = db

class Annotation(Model):
    
    key = CharField()
    value = CharField()

    class Meta:
        database = db

class Variant2Annotation(Model):

    variant = ForeignKeyField(Variant)
    annotation = ForeignKeyField(Annotation)

    class Meta:
        database = db

@begin.start
def main(vcffile: "path to vcf file"):

    vcfreader = vcf.Reader(open(vcffile, 'r'))
    
    annot_name = re.split("\s\|\s",
                          re.search("\'(.+)\'",
                                    vcfreader.infos["ANN"].desc).group(1))
    db.connect()
    db.create_tables([Variant, Annotation, Variant2Annotation], safe=True)

    with db.transaction():
        for record in vcfreader:
            v, insert = Variant.create_or_get(chrom=record.CHROM,
                                  pos=record.POS,
                                  ref=record.REF, 
                                  alt=record.ALT)
            
            for index, value in enumerate(re.split("\s*\|\s*", 
                                                   record.INFO["ANN"][0])):
                a, _ = Annotation.create_or_get(key=annot_name[index],
                                                value=value)
                Variant2Annotation.create_or_get(variant=v.id, annotation=a.id)
