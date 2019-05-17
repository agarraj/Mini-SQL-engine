from readMetadata import readMetadata
import sys

def aggregate(columnName,tableName):
	metadataDict = {}
	metadataDict=readMetadata()

	fun=columnName[:columnName.index("(")]
	columnName=columnName[columnName.index("(")+1:].strip()[:-1]

	if "." in columnName:
		columnName=columnName[columnName.index(".")+1:]
	tName = tableName.strip() + '.csv'

	index=metadataDict[tableName].index(columnName)-1

	colList = []
	fp=open(tName,"r")
	for data in fp:
		colList.append(int(data.replace("\"","").replace("\n","").split(",")[index]))
	#print colList

	print "Output:"
	print fun+"("+tableName+"."+columnName+")"
	
	if fun.lower() == 'min':
		print min(colList)
	elif fun.lower() == 'max':
		print max(colList)
	elif fun.lower() == 'sum':
		print sum(colList)
	elif fun.lower() == 'avg':
		print float(sum(colList))/len(colList)
	elif fun.lower() == 'count':
		print len(colList)
