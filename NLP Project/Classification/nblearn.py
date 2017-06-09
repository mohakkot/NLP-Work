#!/usr/bin/python
import sys
import re
from decimal import *

input_arguments = sys.argv
addition_wp_count = 0
subtraction_wp_count = 0
file_model = open("nbmodel.txt", "w+")
if len(input_arguments) != 3:
	print ("Wrong input")
else:
	vocab = dict()
	conditional_prob = dict()
	ignore_tags = ['NN', 'CN', 'QT', 'PN', 'FF']
	#ignore_tags = ['NN', 'CN', 'QT', 'PN']
	#ignore_words = ['आहेत', 'किती', 'आहे']
	ignore_words = []
	file_labels = open(input_arguments[2], 'r')
	for line in open(input_arguments[1],'r').readlines():
	
		file2_line = file_labels.readline()
		identifier_class = file2_line.strip().split(' ')
		identifier2 = identifier_class[0]
		
		classes = identifier_class[1]
		if classes == "addition":
			addition_wp_count += 1
		elif classes == "subtraction":
			subtraction_wp_count += 1
		label_list = line.strip().split(' ')
		
		identifier1 = label_list[0]
		for i in range(1, len(label_list)):
			word_tag = label_list[i].strip().split("/")
			if word_tag[1] not in ignore_tags and word_tag[0] not in ignore_words:
				if word_tag[0] not in vocab:
					vocab[word_tag[0]] = [0, 0]
				if classes == "addition":
					get_list = vocab[word_tag[0]]
					get_list[0] += 1
				elif classes == "subtraction":
					get_list = vocab[word_tag[0]]
					get_list[1] += 1
				vocab[word_tag[0]] = get_list
	
	total_number_of_words = len(vocab)

	
	#Calculate Priors
	addition_prior = Decimal(addition_wp_count)/Decimal(addition_wp_count + subtraction_wp_count)
	addition_prior = round(addition_prior, 6)
	
	subtraction_prior = Decimal(subtraction_wp_count)/Decimal(addition_wp_count + subtraction_wp_count)
	subtraction_prior = round(subtraction_prior, 6)
	
	prior_string = "prior"+ " " + str(addition_prior) + " " + str(subtraction_prior) + "\n"
	file_model.write(prior_string)
	
	#Calculate Smoothing Denominators
	addition_count_smoothing = 0
	subtraction_count_smoothing = 0
	
	for key in vocab:
		get_list = vocab[key]
		addition_count_smoothing += get_list[0]
		subtraction_count_smoothing += get_list[1]
	
	addition_denominator_smoothing = addition_count_smoothing + total_number_of_words
	subtraction_denominator_smoothing = subtraction_count_smoothing + total_number_of_words
	
	#Calculate Conditional Probability
	for key in vocab:
		get_list = vocab[key]
		addition_word_prob = Decimal(get_list[0] + 1)/Decimal(addition_denominator_smoothing)
		addition_word_prob = round(addition_word_prob, 6)
		
		subtraction_word_prob = Decimal(get_list[1] + 1)/Decimal(subtraction_denominator_smoothing)
		subtraction_word_prob = round(subtraction_word_prob, 6)

		conditional_prob[key] = [addition_word_prob, subtraction_word_prob];
		
	
	
	
	for key in vocab:
		print_line = key + " " + str(conditional_prob[key][0]) + " " + str (conditional_prob[key][1])  + "\n"
		file_model.write(print_line)
	file_model.close()
