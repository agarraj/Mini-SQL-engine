import sys
from readMetadata import readMetadata

def error_handling(query,colNames,tableNames):
	metadataDict = {}
	metadataDict=readMetadata()

	if not "from" in query:
		sys.exit("Invalid query.")
	if not "select" in query:	
		sys.exit("Invalid query.")

	count = query.count("distinct")
	if count>1:
		sys.exit("Error:Multiple distinct")		

	for i in tableNames:
		#print i
		if i not in metadataDict.keys():
			sys.exit("Table not found:"+i)		

	for i in colNames:
		if len(colNames)==1 and colNames[0]=="*":
			pass
			return
		if "(" in i:
			i=i[i.index("(")+1:].strip()[:-1]
			#print i

		if "." in i:
			table=i.split(".")[0].strip()
			i=i.split(".")[1].strip()
			
			#print table	
			if i not in metadataDict[table]:
				#print i
				sys.exit("Column not found:"+i)
		else:		
			count=0
			for j in tableNames:
				if i in metadataDict[j]:
					count+=1
			if count==0:
				#print "hello"+ count
				sys.exit("Column not found:"+i)
			elif count>1:
				sys.exit("Column present in multiple tables.")

			
