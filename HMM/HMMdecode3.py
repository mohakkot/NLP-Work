import sys
import math
import operator

def find_tags(lines):

    for line in lines:
        words = line.split()
        statepos = 0
        prevtag = 'q0'
        back_pointer = {}
        probability = {}
        for word in words:
            if word not in ems:
                for t in tgc:
                    argmax = -(sys.maxsize) - 1
                    if prevtag == 'q0':
                        tran_val = math.log10(trn['q0'][t])
                        if t == 'ZZ':
                            tran_val = 1
                        if statepos not in probability:
                            probability[statepos] = {}
                            probability[statepos][t] = tran_val
                        else:
                            probability[statepos][t] = tran_val
                        if statepos not in back_pointer:
                            back_pointer[statepos] = {}
                            back_pointer[statepos][t] = 'q0'
                        else:
                            back_pointer[statepos][t] = 'q0'
                    else:
                        if prevtag not in ems:
                            prevtaglist = tgc.keys()
                        else:
                            prevtaglist = ems[prevtag]
                        for p in prevtaglist:
                            if trn[p][t] == 0:
                                tran_val = probability[statepos - 1][p]
                            else:
                                tran_val = probability[statepos - 1][p] + math.log10(trn[p][t])
                            if argmax < tran_val:
                                argmax = tran_val
                                if statepos not in probability:
                                    probability[statepos] = {}
                                    probability[statepos][t] = tran_val
                                else:
                                    probability[statepos][t] = tran_val
                                if statepos not in back_pointer:
                                    back_pointer[statepos] ={}
                                    back_pointer[statepos][t] = p
                                else:
                                    back_pointer[statepos][t] = p
            else:
                for t in ems[word]:
                    argmax = -(sys.maxsize) - 1
                    if prevtag != 'q0':
                        if prevtag not in ems:
                            prevtaglist = tgc.keys()
                        else:
                            prevtaglist = ems[prevtag]
                        for p in prevtaglist:
                            if trn[p][t] == 0:
                                tran_val = probability[statepos - 1][p]  + math.log10(ems[word][t])
                            else:
                                tran_val = probability[statepos - 1][p] + math.log10(ems[word][t] * trn[p][t])
                            if argmax < tran_val:
                                argmax = tran_val
                                if statepos not in probability:
                                    probability[statepos] = {}
                                    probability[statepos][t] = tran_val
                                else:
                                    probability[statepos][t] = tran_val
                                if statepos not in back_pointer:
                                    back_pointer[statepos] = {}
                                    back_pointer[statepos][t] = p
                                else:
                                    back_pointer[statepos][t] = p
                    else:
                        tran_val =  math.log10(trn['q0'][t] * ems[word][t])
                        if statepos not in probability:
                            probability[statepos] = {}
                            probability[statepos][t] = tran_val
                        else:
                            probability[statepos][t] = tran_val
                        if statepos not in back_pointer:
                            back_pointer[statepos] = {}
                            back_pointer[statepos][t] = 'q0'
                        else:
                            back_pointer[statepos][t] = 'q0'
            statepos += 1
            prevtag = word

        stats = probability[statepos - 1]
        s = max(stats.items(), key=operator.itemgetter(1))[0]
        str = words[statepos - 1] + '/' + s
        try:
            for i in range(len(words) - 2, -1, -1):
                s = back_pointer[i + 1][s]
                str += ' ' + words[i] + '/' + s
        except:
            pass
        combine = ' '.join(reversed(str.split()))
        fw.write(combine + '\n')




if len(sys.argv) != 2:
    print("Error: Please enter the Training File path")
    sys.exit(1)
path = sys.argv[1]
#path =  'catalan_corpus_dev_raw.txt'
file = open(path, 'r', encoding = 'utf8')
lines  = file.readlines()
file.close()

fw = open('hmmoutput.txt', 'w')

file = open('hmmmodel.txt', 'r')
data = file.readlines()
file.close()
ems = eval(data[0])     #emissions] probability from model file
trn = eval(data[1])     #transition probability from model file
tgc = eval(data[2])     #tagcount from model file

find_tags(lines)        #function to find tags

