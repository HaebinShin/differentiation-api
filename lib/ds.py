def class_sort(class_list):
	tostring_list=[]
	for now in class_list:
		#print now
		tostring_list.append(str(now))
	tostring_list.sort()

	tostring_list_idx={}
	idx=0
	for nowstring in tostring_list:
		tostring_list_idx[nowstring]=idx
		idx+=1

	result=[]
	for i in range(len(class_list)):
		result.append(0)
	
	for now in class_list:
		toidx=tostring_list_idx[str(now)]
		result[toidx]=now
	#print "sort result : ", result
	return result
