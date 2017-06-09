import sys
import json
import math
import re

def classify(file):

    frw = open(file, 'r')
    lines = frw.readlines()
    for obj in lines:
        words = obj.split(' ')
        final_words = []
        prob_neg = 0
        prob_pos = 0
        prob_true = 0
        prob_decept = 0
        for i in range(1, len(words)):
            if words[i] in punctuations:
               words[i] = ''

        for i in range(1, len(words)):
           if re.search('[0-9]', words[i]):
                words[i] = ''

        for i in range(0, len(words)):
            if words[i] == '' or words[i] == ' ' or words[i] in stopset:
                continue
            else:
                final_words.append(words[i])
        words = final_words

        for wrd in range(len(words)):
            tag = words[0]
            for current in range(1, len(words)):
                if words[current] not in stopset:
                    if words[current] in train_data["true_rev"]:
                        prob_true += math.log(train_data["true_rev"][words[current]], 10)
                    if words[current] in train_data["decept_rev"]:
                        prob_decept += math.log(train_data["decept_rev"][words[current]], 10)
                    if words[current] in train_data["pos_rev"]:
                        prob_pos += math.log(train_data["pos_rev"][words[current]], 10)
                    if words[current] in train_data["neg_rev"]:
                        prob_neg += math.log(train_data["neg_rev"][words[current]], 10)

            if prob_true > prob_decept:
                kind = 'truthful'
            else:
                kind = 'deceptive'
            if prob_pos > prob_neg:
                value = 'positive'
            else:
                value = 'negative'
            fwrite.write(tag + ' ' + kind + ' ' + value + '\n')
            break
    fwrite.close()



if len(sys.argv) != 2:
    print("Error: Please enter the classifying File")
    sys.exit(1)

path = sys.argv[1]

file = open("Stop.txt", "r")
stopset = file.read().split('\n')

punctuations=['.',',',';','?','!','[',']','/',':','*','&','+','=','_','(',')','/','@','~','-','"']

frw = open(r"nbmodel.txt", 'r')
train_data = json.load(frw)
frw.close()
fwrite = open(r'nboutput.txt', 'w')
classify(path)
