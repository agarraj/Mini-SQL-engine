from readMetadata import readMetadata
from colIndex import col_index
import re

def whereEvaluate(whereCond,tableNames,table_data):
	metadataDict = {}
	metadataDict=readMetadata()

	andflag=0
	orflag=0

	if "AND" in whereCond:
		whereCond=whereCond.replace("AND","and")
	if "OR" in whereCond:
		whereCond=whereCond.replace("OR","or")
			
	if "and" in whereCond:
		andflag=1
	if "or" in whereCond:
		orflag=1
	
	conditions=[]
	if "and" in whereCond:
		conditions=whereCond.strip().split("and")
	elif "or" in whereCond:
		conditions=whereCond.strip().split("or")
	else:
		conditions.append(whereCond)	
		
	#print conditions

	index_list=colindex(conditions,tableNames)
	
	temp=re.sub("[\s\w\d]",",",whereCond)
	temp=temp.replace(".","")
	op_lst=re.sub("[,]+",",",temp)
	op_lst= op_lst[1:-1].split(",")
	final_list=[]
	for x in table_data:
		x=str(x).split(",")
		if andflag==0 and orflag==0:
			cond1=exp_eval(x,index_list[0],op_lst[0]);
			if cond1:
				final_list.append(x)
		elif andflag==1:
			cond1=exp_eval(x,index_list[0],op_lst[0]);
			cond2=exp_eval(x,index_list[1],op_lst[1]);
			if cond1 and cond2:
				final_list.append(x)
		elif orflag==1:
			#print x
			#print index_list[0]
			#print op_lst[0]
			#print cond1,cond2
			cond1=exp_eval(x,index_list[0],op_lst[0]);
			cond2=exp_eval(x,index_list[1],op_lst[1]);
			#print cond1,cond2
			if cond1 or cond2:
				final_list.append(x)
	return final_list

def exp_eval(x,ls,op):
	if op=="!=" or op=="<>":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][1:])<>int(x[int(ls[1])])
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])<>int(ls[1][1:])
			else:
				return int(x[int(ls[0])])<>int(x[int(ls[1])])
	if op=="<=":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][1:])<=int(x[int(ls[1])])
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])<=int(ls[1][1:])
			else:
				return int(x[int(ls[0])])<=int(x[int(ls[1])])
	if op==">=":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][1:])>=int(x[int(ls[1])])
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])>=int(ls[1][1:])
			else:
				return int(x[int(ls[0])])>=int(x[int(ls[1])])	
	if op==">":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][1:])>int(x[int(ls[1])])
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])>int(ls[1][1:])
			else:
				return int(x[int(ls[0])])>int(x[int(ls[1])])
	if op=="<":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][1:])<int(x[int(ls[1])])
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])<int(ls[1][1:])
			else:
				return int(x[int(ls[0])])<int(x[int(ls[1])])	
	if op=="==" or op== "=":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][1:])==int(x[int(ls[1])])
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])==int(ls[1][1:])
			else:
				return int(x[int(ls[0])])==int(x[int(ls[1])])

	if op== "=-":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][2:])==int(x[int(ls[1])])*(-1)
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])==int(ls[1][2:])*(-1)
			else:
				return int(x[int(ls[0])])==int(x[int(ls[1])])*(-1)	

	if op==">-":
		if str(ls[0])[0]=="v":
			if str(ls[1])[0]=="v":
				pass
			else:
				return int(ls[0][2:])>int(x[int(ls[1])])*(-1)
		else:
			if str(ls[1])[0]=="v":
				return int(x[int(ls[0])])>int(ls[1][2:])*(-1)
			else:
				return int(x[int(ls[0])])>int(x[int(ls[1])])*(-1)					

def colindex(conditions,tableNames):
	index_list=[]
	for i in conditions:
		values=[]
		i=str(i).replace(">=","=").replace("<=","=").replace("!=","=").replace("<>","=").replace(">","=").replace("<","=")
		values=str(i).split("=")
		#print values
		
		index1=-1
		index2=-1

		#if not re.match("[\d]+",values[0]):
		if not re.match("[+,-]?[0-9]+",values[0]):
			#print values[0]
			index1=col_index(tableNames,values[0])
		#print index1
		else:
			index1="v"+values[0]

		#if not re.match("[\d]+",values[1]):
		if not re.match("[+,-]?[0-9]+",values[1]):	
			index2=col_index(tableNames,values[1])
		#print index2
		else:
			index2="v"+values[1]

		index=[index1,index2]
		index_list.append(index)

	return index_list	

