import sys
import collections
import re
from collections import Counter


class document:
	def __init__(self):
		self.words = []
        	self.lable1 = None
        	self.label2 = None
		self.wordcount={}
	def remove_spaces(self,words,stopwords):
		final_words=[]
		for i in range(0,len(words)):
			if words[i]=='' or words[i]==' ' or words [i] in stopwords:
				#print "yes"
				continue
			else:
				final_words.append(words[i])
		self.words=final_words
		self.words=final_words
		#print self.words
	def count(self,words,wordcount):
		wordcount=Counter(words)
		self.wordcount=wordcount
		#print self.wordcount

class preprocessing:
	def tokenize(self,file1,file2):
		file12=open("example.txt","r")
		
		
		
		stopwords=file12.read().split('\n')
		#print line
		tokens=[]
		reviews=[]
		labels=[]
		positive=0
		negative=0
		truth=0
		decep=0
		total_positive=0
		total_neg=0
		total_dec=0
		total_truth=0
		
		for line in file2.readlines():
			columns=line.split("\n")
			c=columns[0].split(" ")
			#print c
			labels.append(c)
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
			for j in range(0,len(d.words)):
				d.words[j]=d.words[j].lower()
			#print d.words
			d.words[0]=d.words[0].replace(d.words[0],' ')
			#for j in range(0,len(d.words)):
				#print j
			#	if numbers(d.words[j]) and letter(d.words[j]):
					 	
			#		d.words[j]=d.words[j].replace(d.words[j],' ')
					#d.words = d.words[:j] + d.words[j+1:]
			#print d.words
			
			for j in range(0,len(d.words)):
				if numbers(d.words[j]):
					d.words[j]=d.words[j].replace(d.words[j],' ')
			tokens.append(d) 
			d.label1=labels[i][1]
			d.label2=labels[i][2]
		#print tokens
		
		for i in range(0,len(tokens)):
			tokens[i].remove_spaces(tokens[i].words,stopwords)

		for i in range(0,len(tokens)):
			tokens[i].count(tokens[i].words,tokens[i].wordcount)
		
		#for i in range(0,len(tokens)):
		#	print tokens[i].wordcount
		#	print tokens[i].label1
		#	print tokens[i].label2
		for i in range(0,len(tokens)):
			if tokens[i].label2=='positive':
				positive=positive+1
			if tokens[i].label2=='negative':
				negative=negative+1
			if tokens[i].label1=='truthful':
				truth=truth+1
			if tokens[i].label1=='deceptive':
				decep=decep+1
		prior_pos=positive/float(len(tokens))
		prior_neg=negative/float(len(tokens))
		prior_truth=truth/float(len(tokens))
		prior_dec=decep/float(len(tokens))


		
		#print positive ,decep
		fe={}	
		features_positive={}
		features_neg={}
		features_dec={}
		features_truth={}
		for i in range(0,len(tokens)):
			if tokens[i].label2=='positive':
				for j in range(0,len(tokens[i].words)):
					if tokens[i].words[j] not in features_positive.keys():
						features_positive[tokens[i].words[j]]=1+tokens[i].wordcount[tokens[i].words[j]]
						total_positive=total_positive+features_positive[tokens[i].words[j]]
					else:
						features_positive[tokens[i].words[j]]=features_positive[tokens[i].words[j]]+tokens[i].wordcount[tokens[i].words[j]]			
						total_positive=total_positive+tokens[i].wordcount[tokens[i].words[j]]			
			elif tokens[i].label2=='negative':
				for j in range(0,len(tokens[i].words)):
					if tokens[i].words[j] not in features_neg.keys():
						features_neg[tokens[i].words[j]]=1+tokens[i].wordcount[tokens[i].words[j]]
						total_neg=total_neg+features_neg[tokens[i].words[j]]
					else:
						features_neg[tokens[i].words[j]]=features_neg[tokens[i].words[j]]+tokens[i].wordcount[tokens[i].words[j]]	
						total_neg=total_neg+tokens[i].wordcount[tokens[i].words[j]]			
			if tokens[i].label1=='deceptive':
				for j in range(0,len(tokens[i].words)):
					if tokens[i].words[j] not in features_dec.keys():
						features_dec[tokens[i].words[j]]=1+tokens[i].wordcount[tokens[i].words[j]]
						total_dec=total_dec+features_dec[tokens[i].words[j]]
					else:
						features_dec[tokens[i].words[j]]=features_dec[tokens[i].words[j]]+tokens[i].wordcount[tokens[i].words[j]]	
						total_dec=total_dec+tokens[i].wordcount[tokens[i].words[j]]			
			elif tokens[i].label1=='truthful':
				for j in range(0,len(tokens[i].words)):
					if tokens[i].words[j] not in features_truth.keys():
						features_truth[tokens[i].words[j]]=1+tokens[i].wordcount[tokens[i].words[j]]
						total_truth=total_truth+features_truth[tokens[i].words[j]]
					else:
						features_truth[tokens[i].words[j]]=features_truth[tokens[i].words[j]]+tokens[i].wordcount[tokens[i].words[j]]	
						total_truth=total_truth+tokens[i].wordcount[tokens[i].words[j]]			
		#print "For positive class:",features_positive
		#print "For Negative class:",features_neg
				
		for i in range(0,len(tokens)):
			for j in range(0,len(tokens[i].words)):
				if tokens[i].words[j] in features_positive.keys() and tokens[i].words[j] not in features_neg.keys():
					features_neg[tokens[i].words[j]]=1
					total_neg=total_neg+features_neg[tokens[i].words[j]]
				elif tokens[i].words[j] not in features_positive.keys() and tokens[i].words[j] in features_neg.keys():
					features_positive[tokens[i].words[j]]=1
					total_positive=total_positive+features_positive[tokens[i].words[j]]
		for i in range(0,len(tokens)):
			for j in range(0,len(tokens[i].words)):
				if tokens[i].words[j] in features_truth.keys() and tokens[i].words[j] not in features_dec.keys():
					features_dec[tokens[i].words[j]]=1
					total_dec=total_dec+features_dec[tokens[i].words[j]]
				if tokens[i].words[j] not in features_truth.keys() and tokens[i].words[j] in features_dec.keys():
					features_truth[tokens[i].words[j]]=1
					total_truth=total_truth+features_truth[tokens[i].words[j]]
		#print " After Smoothing"
		#print "For positive class:",features_positive
		#print "For truthful class:",features_truth
		#print "For negative class:",features_neg
		#print "For deceptive class:",features_dec
		#print "Total positive are:",total_positive
		#print "Total truth are:",total_truth
		#print "Total deceptive are:",total_dec
		#print "Total positive are:",total_positive
		#print "Total negative are:",total_neg
		#for i in range(0,len(features_positive)):
		f9=open("nbmodel.txt","w")
		for k in features_neg:
			print features_neg[k]
			features_neg[k]=features_neg[k]/float(total_neg)
		for l in features_positive:
			print features_positive[l]
			features_positive[l]=features_positive[l]/float(total_positive)
		for j in features_truth:
			#print features_neg[k]
			features_truth[j]=features_truth[j]/float(total_truth)
		for m in features_dec:
			#print features_neg[k]
			features_dec[m]=features_dec[m]/float(total_dec)	
		
		#print features_positive
		#print features_neg
		#print features_truth
		#print features_dec
		
		feature_names=[]

		for k in features_truth:
			feature_names.append(k)
		#print feature_names
		#print features_positive['after']
		
		f9.write('prior'+'\t'+str(prior_pos)+'\t'+str(prior_neg)+'\t'+str(prior_truth)+'\t'+str(prior_dec)+'\n')
		for i in range(0,len(feature_names)):
			f9.write(feature_names[i]+'\t')
			#if feature_names[i] in features_positive.keys():
			#	print "yes"
			val=features_positive[feature_names[i]]
			val1=features_neg[feature_names[i]]
			val2=features_truth[feature_names[i]]
			val3=features_dec[feature_names[i]]
			f9.write(str(val)+'\t'+str(val1)+'\t'+str(val2)+'\t'+str(val3)+'\n')
			
		#reviews=re.split('^(?=[^\s]*?[0-9])(?=[^\s]*?[a-zA-Z])[a-zA-Z0-9]*',d1)
	
		#reviews=re.split('; |, |\*|\n',data)
		
			

if __name__ == "__main__":
	f=open(sys.argv[1],'r')
	f1=open(sys.argv[2],'r')
	p=preprocessing()
	p.tokenize(f,f1)


