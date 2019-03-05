import tejupy
#----------------------------------------------------------------------
def removeepsilon(key,prod):
	tejupy.print_mat()
	for k in prod:
		for j in prod[k]:
			if((j == '~') and (k == key)):
				prod[k].remove('~')
				pass
			else:
				for i in range(len(j)):
					if(j[i] == key):
						tmp = ''
						for x in range(len(j)):
							if(x == i):
								pass
							else:
								tmp = tmp + j[x]
						if(tmp != ''):
							prod[k].append(tmp) 
def checkepsilon(prod):
	for key in prod:
		for i in prod[key]:
			if(i == '~'):
				removeepsilon(key,prod)
	return 0
#------------------------------------------------------------------------
def removeadjacent(prod,prodi,ind,key):
	print key,prodi,ind
	prod[key].remove(prodi)
	for i in prod[prodi[ind]] :
		prod[key].append(str(prodi[:ind]+i))

def checkadjacent(prod):
	for key in prod:
		for i in prod[key]:
			for j in range(len(i)-1):
				if(i[j].isupper() and i[j+1].isupper()):
					removeadjacent(prod,i,j+1,key)
#------------------------------------------------------------------------
def leftrecur():
	file = open('input.txt')
	t = file.read().splitlines()
	production=[]
	num=len(t)
	file_op=open('input.txt' , 'w')
	for comp in t:
		comp+='0'
		production=production+[comp]
	index=3
	for i in range(num):  
		nt=production[i][0]
		if(nt==production[i][index]):
			alpha=production[i][index+1]
			while((production[i][index]!= '0') and (production[i][index]!='|') ):
				index=index+1
			if(production[i][index] != '0'):
				beta=production[i][index+1]
				file_op.write(nt+"->"+beta+nt+"'\n")
				file_op.write(nt+"'"+"->"+alpha+nt+"'"+"|~\n")
			else:
				file_op.write('Cannot be reduced')
		else:
			file_op.write(str(production[i][:-1] + '\n'))
		index=3
#--------------------------------------------------------------------------------------
def leading(key,prod):
	res  =set()
	for i in prod[key]:
		if(i[0].isupper() and i[0]!=key and len(i)>1):
			res = res.union(leading(i[0],prod))
			res = res.union(i[1])
		elif(i[0].isupper() and i[0]!=key):
			res = res.union(leading(i[0],prod))
		elif(i[0].isupper() and i[0]==key and len(i)>1):
			res = res.union(i[1])
		elif(not(i[0].isupper())):
			res = res.union(i[0])
	return res
def trailing(key,prod):
	res  =set()
	for i in prod[key]:
		if(i[-1].isupper() and i[-1]!=key and len(i)>1):
			res = res.union(trailing(i[-1],prod))
			res = res.union(i[-2])
		elif(i[-1].isupper() and i[-1]!=key):
			res = res.union(trailing(i[-1],prod))
		elif(i[-1].isupper() and i[-1]==key and len(i)>1):
			res = res.union(i[-2])
		elif(not(i[-1].isupper())):
			res = res.union(i[-1])
	return res
#--------------------------------------------------------------------
def terminalandvariables(prod):
	global t,nt
	t = set()
	nt =set()
	for key in prod:
		nt = nt.union(key)
		for i in prod[key]:
			for j in i:
				if(j.isupper()):
					nt = nt.union(j)
				else:
					t = t.union(j)
	list(nt).sort()
	list(t).sort()
#--------------------------------------------------------------------
def print_table(ter_map,mat):
	n = len(mat)
	print 'X\t',
	tmp = []
	for key in ter_map :
		print key,'\t',
		tmp.append(key)
	print 
	for i in range(n):
		print tmp[i],'\t',
		for j in range(n):
			print mat[i][j],'\t',
		print 
def parsing_table(prod,start,leading_dic,trailing_dic,nt,t):
	t = t.union('$')
	n = len(t)
	ter_map = {}
	ind = 0 
	for i in t:
		ter_map[i]  = ind
		ind = ind  + 1
	mat = [['-' for i in range(n)]for j in range(n)]
	for i in leading_dic[start]:
		mat[ter_map['$']][ter_map[i]]='<'
	for i in trailing_dic[start]:
		mat[ter_map[i]][ter_map['$']] = '>'
	for key in prod:
		for i in prod[key]:
			if(len(i)==1):
				pass
			else:
				for j in range(len(i)-1):
					if(i[j] in t and i[j+1] in nt):
						for x in leading_dic[i[j+1]]:
							mat[ter_map[i[j]]][ter_map[x]] = '<' if mat[ter_map[i[j]]][ter_map[x]] == '-' else mat[ter_map[i[j]]][ter_map[x]]

					elif(i[j+1] in t and i[j] in nt):
						for x in trailing_dic[i[j]]:
							mat[ter_map[x]][ter_map[i[j+1]]] = '>' if mat[ter_map[x]][ter_map[i[j+1]]] == '-' else mat[ter_map[x]][ter_map[i[j+1]]] 
	for key in prod:
		for i in prod[key]:
			if(len(i) == 3):
				for j in range(len(i)-2):
					if(i[j] in t and i[j+2] in t):
						mat[ter_map[i[j]]][ter_map[i[j+2]]] = '='
	

def main():
	f = open('input.txt')
	input_file = f.read().splitlines()
	prod = {}
	global start
	start  = input_file[0][0]
	for i in input_file:
		tmp = i.split('->')
		prod[tmp[0]]  = tmp[1].split('|')
		
	terminalandvariables(prod)
	checkepsilon(prod)
	checkadjacent(prod)
	global leading_dic,trailing_dic
	leading_dic = {}
	trailing_dic = {}
	for key in prod:
		trailing_dic[key] = list(trailing(key,prod))
		trailing_dic[key].sort()
		leading_dic[key] = list(leading(key, prod))
		leading_dic[key].sort()
	# print leading_dic
	# print trailing_dic
	# print t
	# print nt
	print "----------------PARSING TABLE-------------------"
	parsing_table(prod,start,leading_dic,trailing_dic,nt,t)
main()
