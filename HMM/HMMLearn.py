import sys

wordlist =[]            #used for keeping the words of a line
tagsofword={}           #used for count of a tags for all the words
tagcount={}             #total instances of a tag
statetrans = {}         #used for keeping the count of transitions between various states
allwords = []           #keep all the words not seperated from tags


#computing the final probabilities of the all the words:

def compute_prob(path):

    file = open(path,'r', encoding="utf8")
    line = file.readlines()
    create_list(line)
    compute_emission()
    compute_transition(line)
    file.close()


#creates the list of all the words in every sentence

def create_list(lines):
    for line in lines:
        words = line.split()
        for word in words:
            allwords.append(word)


#computing the emission probabilities of the all the words using formula:
#            count of number of times a single tag assigned to a word
# emission = --------------------------------------------------------
#            total number of tag in which the word is classified

def compute_emission():

    for word in allwords:
        word_split = word.split('/')
        tag = word_split[len(word_split)-1]
        currword = "/".join(word_split[0:len(word_split)-1])

        if currword not in tagsofword.keys():
            wordlist.append(currword)
            tagsofword[currword]= {}
            tagsofword[currword][tag] = 1
        else:
            if tag not in tagsofword[currword].keys():
                tagsofword[currword][tag] = 1
            else:
                tagsofword[currword][tag] +=1
        if tag not in tagcount:
            tagcount[tag] = 1
        else:
            tagcount[tag] +=1

    for word in tagsofword.keys():
        for t in tagsofword[word]:
            tagsofword[word][t] = ((tagsofword[word][t] * 1.0) / (tagcount[t]))



#computing the transition probabilities of the all the states:

def compute_transition(lines):

    for line in lines:
        prevstate = ''
        words = line.split()
        for w in words:
            word_split = w.split('/')
            tag = word_split[len(word_split) - 1]

            if prevstate == '':
                currstate = 'q0'
            else:
                currstate = prevstate

            if currstate not in statetrans.keys():
                statetrans[currstate]={}
                statetrans[currstate][tag] = 1
            else:
                if tag not in statetrans[currstate].keys():
                   statetrans[currstate][tag] = 1
                else:
                    statetrans[currstate][tag] += 1
            prevstate = tag
# doing smoothing
    for states in statetrans.keys():
        chk = 0
        for tgs in tagcount:
            if tgs not in statetrans[states].keys():
                statetrans[states][tgs] = 0
                chk += 1
        if chk > 0:
            for tgs in statetrans[states].keys():
                statetrans[states][tgs] += 1

        fincnt = sum(statetrans[states].values())
# calculate the transition probability
        for tgs in statetrans[states].keys():
            if states == 'q0':
                statetrans[states][tgs] = (statetrans[states][tgs] * 1.0) / (fincnt)
            else:
                statetrans[states][tgs] = (statetrans[states][tgs] * 1.0) / (fincnt)


if len(sys.argv) != 2:
    print("Error: Please enter the Training File path")
    sys.exit(1)

path_train = sys.argv[1]
#path_train = 'catalan_corpus_train_tagged.txt'
file = open("hmmmodel.txt", 'w')
compute_prob(path_train)
file.write(str(tagsofword))
file.write('\n')
file.write(str(statetrans))
file.write('\n')
file.write(str(tagcount))
file.close()