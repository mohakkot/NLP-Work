

import sys
import collections
import re
from collections import Counter
import random
class document:
	def __init__(self):
		self.words = []
        	self.lable1 = None
        	self.label2 = None
		self.wordcount={}	
		self.id=None
	def remove_spaces(self,words):
		final_words=[]
		for i in range(0,len(words)):
			if words[i]=='' or words[i]==' ':
				#print "yes"
				continue
			else:
				final_words.append(words[i])
		self.words=final_words
		#print self.words

class preprocessing:
	def tokenize(self,file1):
		tokens=[]
		reviews=[]

		
		punctuations=['.',',',';','?','!','[',']','/',':','*','&','+','=','_','(',')','/','@','~','-','"']
		data=file1.read().rstrip('\n')
		#re.sub( '\s+', ' ', data).strip()
		data1=data.split('\n')
		def numbers(inputString):
			return bool(re.search('[0-9]', inputString))
		def letter(inputString):
			return bool(re.search('[a-zA-Z]', inputString))
		#print "data is :"
		for element in data1:
			for ele in element:
				if ele in punctuations:
					element=element.replace(ele,' ')
					
			#print "here it is:",element
			reviews.append(element)
		#print "yooo",reviews
		
		for i in range(0,len(reviews)):
			d=document()
			d.words=reviews[i].split(" ")
			#print d.words
			d.id=d.words[0]
			for j in range(0,len(d.words)):
				#print j
				
				if numbers(d.words[j]) and letter(d.words[j]):
						
					d.words[j]=d.words[j].replace(d.words[j],' ')
					#d.words = d.words[:j] + d.words[j+1:]
					
			for j in range(0,len(d.words)):
				d.words[j]=d.words[j].lower()
			#print d.words
			
			
			#print d.words
			
			for j in range(0,len(d.words)):
				if numbers(d.words[j]):
					d.words[j]=d.words[j].replace(d.words[j],' ')
			tokens.append(d)

		for i in range(0,len(tokens)):
			tokens[i].remove_spaces(tokens[i].words)


		#for i in range(0,len(tokens)):
		#	print tokens[i].words
	
		g=open("nbmodel.txt","r")
		model={}
		for line in g.readlines():
			h=line.split('\n')
			for char in h:
				split2=char.split('\t')
				#print split2
				if len(split2)>=4:
					
					model[split2[0]]=[]
					model[split2[0]].append(split2[1])
					model[split2[0]].append(split2[2])
					model[split2[0]].append(split2[3])
					model[split2[0]].append(split2[4])
		#print model

		file=open("nboutput.txt","w")
		
		for i in range(0,len(tokens)):
			probability_positive=1
			probability_neg=1
			probability_truth=1
			probability_dec=1
			for j in range(0,len(tokens[i].words)):
			
				if tokens[i].words[j] in model :
						probability_positive=probability_positive*float(model[tokens[i].words[j]][0])
						probability_neg=probability_neg*float(model[tokens[i].words[j]][1])
						probability_truth=probability_truth*float(model[tokens[i].words[j]][2])
						probability_dec=probability_dec*float(model[tokens[i].words[j]][3])
			print tokens[i].id
			if probability_positive >= probability_neg and probability_truth >= probability_dec:
				#ran=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(20))
		
				file.write(tokens[i].id+' '+'truthful'+' '+'positive'+'\n')
			if probability_neg >= probability_positive and probability_truth >= probability_dec:
				#ran=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(20))
		
				file.write(tokens[i].id+' '+'truthful'+' '+'negative'+'\n')
				#print "Class label Negative"
			if  probability_positive >= probability_neg and probability_dec >= probability_truth:
				#ran=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(20))
		
				file.write(tokens[i].id+' '+'deceptive'+' '+'positive'+'\n')
			if  probability_neg >= probability_positive and probability_dec >= probability_truth:
				#ran=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(20))
		
				file.write(tokens[i].id+' '+'deceptive'+' '+'negative'+'\n')


		














if __name__ == "__main__":
	f=open(sys.argv[1],'r')
	p=preprocessing()
	p.tokenize(f)
