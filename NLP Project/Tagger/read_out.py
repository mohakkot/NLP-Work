#subroutine formatting output of the TNT tagger
def combine_questions(lines):
    problem = ''
    l =1
    for line in lines:
        if line[0:2] == '%%':
            continue
        words= line.strip().split('\t')
        if words[0] == 'START':
            problem = ''
        elif words[0].find("WP") != -1:
            problem = problem + words[0]
        elif words[0] == 'END':
            if l == 1:
                fw.write(problem)
            else:
                fw.write('\n'+problem)
            l = 2
        else:
            problem = problem + " " + "".join(w for w in words if w !='')

#output of the TNT tagger ran on test file
fr  = open('out.txt', 'r', encoding="utf8")
data = fr.readlines()
fr.close()
#Final file of Test corpus after tagging
fw = open('file_out.txt', 'w', encoding="utf8")
combine_questions(data)
fw.close()
