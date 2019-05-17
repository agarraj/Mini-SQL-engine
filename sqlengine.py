import sqlparse
import sys
import re
from readMetadata import readMetadata
from where import whereEvaluate
from colIndex import col_index
from aggregate import aggregate
from error import error_handling
from projection import project

def main():
	metadataDict = {}
	metadataDict=readMetadata()
	query=str(sys.argv[1])

	evaluateQuery(query,metadataDict)

def evaluateQuery(query,metadataDict):
	for stmnt_unformated in sqlparse.parse(query):
	    statement = sqlparse.parse(
	        			sqlparse.format(
	            			str(stmnt_unformated)
	        				)
	    				)[0]

	query_tokens=[]	
	for x in statement.tokens:
		if re.match('([\s]+)', str(x)):
			continue
		else:
			query_tokens.append(str(x));	 

	#print query_tokens

	distinct_flag=0
	distinct_flag2=0
	if str(query_tokens[1]).lower() == "distinct":
		distinct_flag=1
	elif "distinct(" in query:
	 	distinct_flag2=1
	#print distinct_flag2		

	colNames=query_tokens[1+distinct_flag].split(",")
	#print colNames
	tableNames=query_tokens[3+distinct_flag].split(",")
	#print tableNames

	#Error Handling
	error_handling(query,colNames,tableNames)

	#Checking for aggregate function
	func=["min","max","count","sum","avg"]
	if any(x in query for x in func):
		aggregate(colNames[0],tableNames[0])
		return

	#reading table data from file
	temp_table_data=[]
	table_data=[]
	cross=[]
	for t in tableNames:
		f = open(t+".csv",'r')
		temp_table_data=[line.replace('"', '').strip() for line in f]

		if len(table_data)==0:
			table_data=temp_table_data
		else:
			for y in temp_table_data:
				for z in table_data:
					cross.append(z+","+y)

			table_data=cross;
			cross=[]
	#print table_data

	#Checking for Where Condition 
	index = 4+distinct_flag
	if len(query_tokens) > index:
		whereCond=""
		whereCond=query_tokens[index][6:]
		#print whereCond

		table_data=whereEvaluate(whereCond,tableNames,table_data)

	#Projection
	table_data=project(colNames,tableNames,table_data)

	if distinct_flag==1 or distinct_flag2==1:
	 	table_data=[table_data[0],distinct(table_data[1])]

	# for x in table_data:
	# 	print table_data 	
	#Printing Output
	print "Output:"
	header=""
	flag=0
	for i in table_data[0]:
		if flag==0:
			header+=str(i)
			flag=1
		else:	
			header=header+","+str(i)
	print header

	for x in table_data[1]:
		flag=0
		valstr=""
		if isinstance(x,list):
			for y in x:
				#print y
				if flag==0:
					valstr=valstr+str(y)
					flag=1
				else:
					 valstr=valstr+","+str(y)
			#print valstr	
		else:	
			if flag==0:
					valstr=valstr+str(x)
					flag=1
			else:
				 valstr=valstr+","+str(x)
		print valstr	 	 	
		

def distinct(table_data):
	temp_data=[]
	for line in table_data:
		if line not in temp_data:
			temp_data.append(line)
	return temp_data			


if __name__ == "__main__":
	main()