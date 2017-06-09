import subprocess

#subroutine to format the taining file
def createfile(lines):
    start = 'START  /ST'
    end = 'END  /EN'
    fw.write(start + '\n')
    for line in lines:
        words = line.strip().split()
        chk = True
        for wrd in words:
            if chk == True:
                currword = wrd + '\t' + '/' + 'TG'
                chk = False
            else:
                word_split = wrd.split('/')
                tag = word_split[len(word_split) - 1]
                currword = word_split[0] + '\t' + '/' + tag
            fw.write(currword)
            fw.write('\n')
        fw.write(end+'\n')

#subroutine to format test file
def format_file(lines):
    start = 'START  /ST'
    end = 'END  /EN'
    for line in lines:
        words = line.strip().split()
        fw1.write(start + '\n')
        for wrd in words:
            fw1.write(wrd)
            fw1.write('\n')
        fw1.write(end + '\n')


#subroutine to run all Linux codes
def run_linux():
    var = subprocess.call(['./tnt-para', 'tagged_file.txt'])
    if var != 0:
        print('error in execution')
    ans = subprocess.call(['./tnt', 'tagged_file', 'test_file.txt'], stdout = file_out)
    if ans != 0:
        print('Error in execution of test_file')
    prg1 = subprocess.call(['python3', 'read_out.py'])
    if prg1 != 0:
        print('Error in execution of program read_out')


#opening all the files
fw = open('tagged_file.txt', 'w', encoding="utf8")
fw1 = open('test_file.txt', 'w', encoding="utf8")
fr = open('test_corpus.txt','r', encoding="utf8")
file = open('tagged_corpus.txt', 'r', encoding="utf8")
file_out = open('out.txt', 'w', encoding='utf8')

#Tagged Data for Training
data = file.readlines()

#Test data
test_data = fr.readlines()

#Creating file for TNT tagger training
createfile(data)
file.close()
fw.close()

#Formatting test file for inputting too tagger for tagging
format_file(test_data)
fr.close()
fw1.close()

#running TNT tagger and calling program for formatting output file
run_linux()
file_out.close()

