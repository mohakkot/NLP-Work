import sys
import re
import math

input_arguments = sys.argv
if len(input_arguments) != 2:
#if len(input_arguments) != 1:
	print ("Wrong input")
else:
	file_model= open("nbmodel.txt", "r")
	file_test = open(input_arguments[1], 'r')
	#file_test = open("test_tagged_corpus.txt", 'r')
	file_output= open("nboutput.txt", "w+")
	conditional_prob = dict()
	ignore_tags = ['NN', 'CN', 'QT', 'PN', 'FF']
	#ignore_tags = ['NN', 'CN', 'QT', 'PN']
	#ignore_words = ['आहेत', 'किती', 'आहे']
	ignore_words = []
	line_model= file_model.readline()
	priors= line_model.strip().split(' ')
	addition_prior= round(float(priors[1]), 6)
	subtraction_prior= round(float(priors[2]), 6)

	for line in file_model.readlines():
		line= line.strip().split(' ')
		conditional_prob[line[0]]= [round(float(line[1]), 6), round(float(line[2]), 6)]
	#print conditional_prob

	for line in file_test.readlines():
		label_list = line.strip().split(' ')
		multiply_class_addition= math.log(addition_prior)
		multiply_class_subtraction= math.log(subtraction_prior)
		identifier1 = label_list[0]
		#print identifier1
		#print label_list
		for i in range(1, len(label_list)):
			word_tag = label_list[i].strip().split('/')
			#print "0 " + word_tag[0]
			#print "1" + word_tag[1]
			if word_tag[1] not in ignore_tags and word_tag[0] not in ignore_words:
				if word_tag[0] in conditional_prob:
					multiply_class_addition= multiply_class_addition + math.log(conditional_prob[word_tag[0]][0])
					multiply_class_subtraction= multiply_class_subtraction + math.log(conditional_prob[word_tag[0]][1])
		if multiply_class_addition > multiply_class_subtraction:
			wp_class= "addition"
		else:
			wp_class= "subtraction"

		print_string= identifier1+" "+wp_class
		file_output.write(print_string+"\n")

	file_output.close()
