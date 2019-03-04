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
