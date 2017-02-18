import sys 
import vcf 
import re
from model import * 
import peewee

filename = sys.argv[1]
print("import", filename)

reader = vcf.Reader(open(filename,'r'))

#  PARSE HEADERS AND CREATE ANNOTATION TABLE ACCORDING FIELDS NUMBER
for info in reader.infos:
	if info == "ANN":
		desc = reader.infos["ANN"].desc
		bloc = re.findall(r"'(.+)'", desc)
		fields = [i.strip() for i in bloc[0].split("|")]
		for i in range(len(fields)):
			key = info +"_" + str(i+1)
			f = Field(colname = key, desc = fields[i])
			f.save()
			# Append new columns no annotation 
			new_col = peewee.CharField(null=True)
			new_col.add_to_class(Annotation, key)
		# Create annotation table
		Annotation.create_table()

# IMPORT VARIANT AND ANNOTATION DATA
with db.transaction():
	for record in reader:
		variant = Variant.create(chrom = record.CHROM, pos = record.POS, ref = record.REF, alt = record.ALT[0] )
		if "ANN" in record.INFO:
			ann = record.INFO["ANN"]
			m = Annotation()
			m.variant = variant
			i = 1
			for value in ann[0].split("|"):
				key = "ANN_"+str(i)
				setattr(m,key,value)
				i+=1
			m.save()