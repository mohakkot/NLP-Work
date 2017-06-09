import subprocess

def createfile(lines):
    for line in lines:
        words = line.split()
        l = 0
        for wrd in words:
            currword = ''
            l += 1
            word_split = wrd.split('/')
            tag = word_split[len(word_split) - 1]
            currword = word_split[0] + '\t' + '/' + tag
            fw.write(currword)
            if l != len(words)-1:
                fw.write('\n')

def format_file(lines):
    for line in lines:
        words = line.split()
        for wrd in words:
            fw1.write(wrd)
            fw1.write('\n')

def run_linux():
    var = subprocess.call(['./tnt-para', 'tagged_file.txt'])
    if var != 0:
        print('error in execution')
    ans = subprocess.call(['./tnt', 'tagged_file', 'test_file.txt', '>final_tagged.txt'])
    if ans != 0:
        print('Error in execution of test_file')



fw = open('tagged_file.txt', 'w', encoding="utf8")
fw1 = open('test_file.txt', 'w', encoding="utf8")
#fr = open('test_corpus.txt','r', encoding="utf8")
file = open('Tagged-corpus.txt', 'r', encoding="utf8")
data = file.readlines()
test_data = fr.readlines()
createfile(data)
file.close()
fw.close()
format_file(test_data)
#fr.close()
#run_linux()
fw1.close()

