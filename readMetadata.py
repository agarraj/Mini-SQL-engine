def readMetadata():
	metadataDict = {}
	f = open('metadata.txt','r')
	flag = 0
	for line in f:
		line = line.replace('"', '').strip()
		if line.strip() == "<begin_table>":
			flag = 1
			continue
		if flag == 1:
			tblName = line.strip()
			metadataDict[tblName] = [];
			flag = 0
			continue
		if not line.strip() == '<end_table>':
			colName=line.strip()
			metadataDict[tblName].append(colName);

	#metadataDict = {key: metadataDict[key].insert(0,len(value)) for key, value in metadataDict.items()}	
	for keys,values in metadataDict.items():
	    metadataDict[keys].insert(0,len(values))
	
	# for keys,values in metadataDict.items():
	#     print(keys)
	#     print(values)	
	return metadataDict	    	