import sys

input_arguments = sys.argv
ip_file = open("file_out.txt", "r", encoding="utf8")
file_label = open('nboutput.txt', 'r', encoding="utf8")
file_output = open("output.txt", "w", encoding="utf8")

file_data= ip_file.readlines()
fr = file_label.readlines()
labels = {}
i =0
for l in fr:
    lb = l.strip().split()
    labels[i]= lb
    i+=1
i =0
for line in file_data:
    id = line[0]
    ent = ''
    last_adj=''
    pn_dict = {}
    adj_list=[]
    nn_list = []
    last_nn = ''
    j=0
    words = line.strip().split()
    for word in words:
        if word.find("CN") != -1:
            if ent == '':
                ent = word
            elif ent == word:
                continue
            else:
                labels[i][1] = "invalid entity type"
                break

        if word.find("NN") != -1:
            nn_list.append(word)
            last_nn = word

        if word.find("किती") != -1 and last_nn not in nn_list:
            labels[i][1] = "invalid proper noun type"
            break

        if word.find("ADJ") != -1:
            adj_list.append(word)
            last_adj=word
    if i == len(file_data)-1:
        if last_adj not in adj_list and last_adj != '':
            labels[i][1] = "invalid adjective type"
            file_output.write(" ".join(labels[i]))
            i += 1
        else:
            file_output.write(" ".join(labels[i]))
            i += 1
        break
    else:
        if last_adj not in adj_list and last_adj != '':
            labels[i][1] = "invalid adjective type"
            file_output.write(" ".join(labels[i]) +'\n')
            i += 1
        else:
            file_output.write(" ".join(labels[i])+'\n')
            i += 1












