import sys
from collections import Counter
import string
import json
import re

label_dict_truth = {}
label_dict_decept = {}

positive_words = []
negative_words = []
deceptive_words = []
truth_words = []
prior = {}

def readlabel(file):
    cntp = 0
    cntn = 0

    frw = open(file, 'r')
    lines = frw.readlines()
    for obj in lines:
        words = obj.strip().split()
        if words[1] == "deceptive":
            label_dict_decept[words[0]] = words[2]
        else:
            label_dict_truth[words[0]] = words[2]
        if words[2] == 'positive':
            cntp = cntp + 1
        else:
            cntn = cntn + 1
    frw.close()
    prior['p'] = float(cntp / (cntp + cntn))
    prior['n'] = float(cntn / (cntn + cntp))
    prior['t'] = float(len(label_dict_truth) / (len(label_dict_decept) + len(label_dict_truth)))
    prior['d'] = float(len(label_dict_decept) / (len(label_dict_decept) + len(label_dict_truth)))


def findwords(file):

    frw = open(file, 'r')
    lines = frw.readlines()
    for obj in lines:
        final_words = []
        words= obj.split()
        for i in range (1, len(words)):
            j = 0
            while j < len(words[i]):
                if words[i][j] in punctuations:
                    words[i] = words[i].replace(words[i][j], '')
                else:
                    j = j + 1

        for i in range(1, len(words)):
            if re.search('[0-9]', words[i]):
                words[i] = ''

        for i in range(0, len(words)):
            if words[i] == '' or words[i] == ' ' or words[i] in stopset:
                continue
            else:
                final_words.append(words[i])
        words = final_words

        for cnt in range (len(words)):
            if words[cnt] in label_dict_decept.keys():
                if label_dict_decept[words[cnt]] == 'positive':
                    for freq in range(1, len(words)):
                        words[freq] = words[freq].lower()
                        positive_words.append(words[freq])
                        deceptive_words.append(words[freq])
                    break
                else:
                    for freq in range(1, len(words)):
                        words[freq] = words[freq].lower()
                        negative_words.append(words[freq])
                        deceptive_words.append(words[freq])
                    break
            elif words[cnt] in label_dict_truth.keys():
                if label_dict_truth[words[cnt]] == 'positive':
                    for freq in range(1, len(words)):
                        words[freq] = words[freq].lower()
                        positive_words.append(words[freq])
                        truth_words.append(words[freq])
                    break
                else:
                    for freq in range(1, len(words)):
                        words[freq] = words[freq].lower()
                        negative_words.append(words[freq])
                        truth_words.append(words[freq])
                    break
    frw.close()

def findprob():

    train = {}
    train['pos_rev'] = {}
    train['neg_rev'] = {}
    train['true_rev'] = {}
    train['decept_rev'] = {}

    posneg = set(negative_words + positive_words)
    trudec = set(truth_words + deceptive_words)
    negcnt = Counter(negative_words)
    poscnt = Counter(positive_words)
    decptcnt = Counter(deceptive_words)
    truthcnt = Counter(truth_words)
    pw = set(positive_words)
    nw = set(negative_words)
    tw = set(truth_words)
    dw = set(deceptive_words)

    pos_len = len(positive_words)
    neg_len = len(negative_words)
    true_len = len(truth_words)
    decept_len = len(deceptive_words)
    for words in posneg:
        if words in positive_words:
            pos_len = pos_len + 1
        if words in negative_words:
            pos_len = neg_len + 1
        if words in truth_words:
            pos_len = true_len + 1
        if words in deceptive_words:
            pos_len = decept_len + 1

    for words in posneg:
        countT = 1 + truthcnt[words]
        countD = 1 + decptcnt[words]
        countN = 1 + negcnt[words]
        countP = 1 + poscnt[words]

        train['pos_rev'][words] = prior['p'] * (countP * 1.0) / pos_len
        train['neg_rev'][words] = prior['n'] * (countN * 1.0) / neg_len
        train['true_rev'][words] = prior['t'] * (countT * 1.0) / true_len
        train['decept_rev'][words] = prior['d'] * (countD * 1.0) / decept_len

    frw = open(r"nbmodel.txt", 'w')
    json.dump(train, frw)
    frw.close()



#if len(sys.argv) != 3:
#    print("Error: Please enter both the Training File as well as Label File")
#    sys.exit(1)

path_train = 'train-text.txt'#sys.argv[1]
path_label = 'train-labels.txt'#sys.argv[2]

file = open("Stop.txt", "r")
stopset = file.read().split('\n')

punctuations=['.',',',';','?','!','[',']','/',':','*','&','+','=','_','(',')','/','@','~','-','"']

readlabel(path_label)
findwords(path_train)
findprob()
