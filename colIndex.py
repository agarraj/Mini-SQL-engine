from readMetadata import readMetadata
import sys

def col_index(tableNames,colname):
	metadataDict = {}
	metadataDict=readMetadata()

	table=""
	col=""
	if "." in colname:
		table=colname.split(".")[0].strip()
		col=colname.split(".")[1].strip()
	else:
		col=colname.strip()	

	if "distinct(" in col:
		col=col[col.index("(")+1:].strip()[:-1]	

	if(len(table)>0):
		#Error Handling
		if table not in metadataDict.keys():
			sys.exit("Table not found:"+table)	
		i=0
		j=0
		for t in tableNames:
			if t <> table:
				i+=1
			else:
				break

		count=0
		if col in metadataDict[tableNames[i]]:
				count+=1
		if count <> 1:
			sys.exit("Column not found:"+col)

		for p in metadataDict[tableNames[i]]:
			if p <> col:
				j+=1
			else:
				if i>0:
					#print metadataDict[tableNames[i-1]][0]+j-1
					return metadataDict[tableNames[i-1]][0]+j-1
				else:
					#print j-1	
					return j-1

	else:
		#Error Handling
		count=0
		for j in tableNames:
			if col in metadataDict[j]:
				count+=1
		if count==0:
			#print count
			sys.exit("Column not found:"+col)
		elif count>1:
			sys.exit("Column present in multiple tables.")

		i=0
		for x in tableNames:
			j=0
			for p in metadataDict[x]:
				if p <> col:
					j+=1
				else:
					if i>0:
						#print metadataDict[tableNames[i-1]][0]+j-1
						return metadataDict[tableNames[i-1]][0]+j-1
					else:
						#print j-1
						return j-1
			i+=1

				



