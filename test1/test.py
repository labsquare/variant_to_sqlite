import sys 
import vcf 
from model import * 


filename = sys.argv[1]
print("import", filename)

reader = vcf.Reader(open(filename,'rb'))
with db.transaction():
	for record in reader:
		Variant.create(chrom = record.CHROM, pos = record.POS, ref = record.REF, alt = record.ALT[0] )
	  


