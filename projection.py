from readMetadata import readMetadata
from colIndex import col_index

def project(colNames,tableNames,table_data):
	metadataDict = {}
	metadataDict=readMetadata()
	ind_lst=[]
	ind_lst_val=[]
	flag=0
	if len( colNames)==1 and colNames[0]=="*":
		for x in tableNames:
			flag=0
			for y in metadataDict[x]:
				if flag==0:
					flag=1
					continue
				else:
					ind_lst_val.append(x+"."+y)
		return [ind_lst_val,table_data]	

	for i in colNames:
		if "." not in i:
			for j in tableNames:
				if i in metadataDict[j]:
					i=j+"."+i
		ind_lst_val.append(i)
		ind_lst.append(col_index(tableNames,i))
	lst=[]
	#print ind_lst
	#print table_data
	#print table_data
	for x in table_data:
		ls=[]
		if not isinstance(x,list):
			x=x.split(",")
		for y in ind_lst:
			#print x[y]
			ls.append(x[y])
		lst.append(ls)
		#print lst
	return [ind_lst_val,lst]	
