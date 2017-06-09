#!/usr/bin/python
import sys
import re
from decimal import *


def getEnglishNumbers(qt):
    number_dict = dict()
    number_dict = {'१': 1, '२': 2, '३': 3, '४': 4, '५': 5, '६': 6, '७': 7, '८': 8, '९': 9, '०': 0}
    # qt = '३६१'
    number = 0
    for i in range(0, len(qt)):
        if qt[i] in number_dict:
            digit = number_dict[qt[i]]
            # print (digit)
            number = number * 10 + digit

    return number


input_arguments = sys.argv
file_labels = open("output.txt", "r", encoding="utf8")
file_test = open(input_arguments[1], 'r')
file_output = open("final_output", "w+", encoding="utf8")

if len(input_arguments) != 2:
    print("Wrong input")
else:
    positive_verbs = ["मिळाले", "मिळाली", "आणले", "विकत", "घेतल्या", "घेतल्यावर", "ठेवले", "मिळतात", "घेतली", "घेतले",
                      "मिळाल्या", "आणली", "आणल्या", "ठेवल्या", "ठेवली"]

    negative_verbs = ["दिले", "दिली", "दिल्या", "विकले", "राहिले", "देते", "पडली", "खाल्ले", "हरवला", "हरवले", "हरवली",
                      "वापरले", "खाल्ली", "विकल्या", "राहिल्या", "देतो", "पडले", "पडल्या", "खाल्ल्या", "हरवल्या",
                      "वापरली", "वापरल्या", "विकली"]

    for line in file_test.readlines():
        words = line.strip().split(' ')
        line_label = file_labels.readline()
        line_label = line_label.strip().split(' ')
        class_label = line_label[1]
        index_FF = []
        index_QT = []
        num_list = []
        index_VB = []
        verb_list = []
        unknown_index = -1
        unknown_index_ajun = -1
        identifier = words[0]
        if class_label == 'Invalid Word Problem Type':
            file_output.write(" ".join(line_label)+ '\n')
            break

        if class_label.strip() == "addition":
            for i in range(1, len(words)):
                word_tag = words[i].strip().split('/')
                # print (word_tag)
                if (word_tag[1] == "FF"):
                    # print (i)
                    index_FF.append(i)
                elif (word_tag[1] == "QT"):
                    index_QT.append(i)
                    num_list.append(word_tag[0])
                elif (word_tag[0] == "किती"):
                    unknown_index = i

            # Type 3 and type 4 problems (addition)
            # There are 6 frogs in the pond. 2 more frogs hop in the pond. How  many frogs are there in the pond?
            # Rahul has 6 cars. Nikita gave him 9 more cars. How many cars does Rahul have altogether?
            if (len(index_FF) >= 3 and len(index_QT) >= 2):
                if index_FF[0] > index_QT[0] and index_FF[1] > index_QT[1] and unknown_index > index_QT[
                    0] and unknown_index > index_QT[1]:
                    qt1 = getEnglishNumbers(num_list[0])
                    qt2 = getEnglishNumbers(num_list[1])
                    unknown = qt1 + qt2
                    file_output.write(identifier + " " + "x=" + str(qt1) + "+" + str(qt2) + " x=" + str(unknown) + '\n')
                else:
                    file_output.write(identifier + " " + "Invalid addition type" + '\n')

            # Type 6 (addition)
            # William has 5 red cars and 9 blue cars. How many cars does he have in total?
            elif (len(index_FF) >= 2 and len(index_QT) >= 2):
                if index_FF[0] > index_QT[0] and index_FF[0] > index_QT[1] and unknown_index > index_QT[
                    0] and unknown_index > index_QT[1]:
                    qt1 = getEnglishNumbers(num_list[0])
                    qt2 = getEnglishNumbers(num_list[1])
                    unknown = qt1 + qt2
                    file_output.write(identifier + " " + "x=" + str(qt1) + "+" + str(qt2) + " x=" + str(unknown) + '\n')
            else:
                print(identifier + " " + "Invalid addition type")


        elif class_label.strip() == "subtraction":
            for i in range(1, len(words)):
                word_tag = words[i].strip().split('/')
                # print (word_tag)
                if (word_tag[1] == "FF"):
                    # print (i)
                    index_FF.append(i)
                elif (word_tag[1] == "QT"):
                    index_QT.append(i)
                    num_list.append(word_tag[0])
                elif (word_tag[0] == "काही" and unknown_index == -1):
                    unknown_index = i
                elif (word_tag[0] == "थोडी" and unknown_index == -1):
                    unknown_index = i
                elif (word_tag[0] == "थोडे" and unknown_index == -1):
                    unknown_index = i
                elif (word_tag[0] == "किती" and unknown_index == -1):
                    unknown_index = i
                elif (word_tag[1] == "VB"):
                    index_VB.append(i)
                    verb_list.append(word_tag[0])
                elif (word_tag[0] == "अजून" and unknown_index == -1):
                    unknown_index_ajun = i

            if unknown_index_ajun != -1:
                flag = 0
                for j in range(0, len(index_FF)):
                    if index_FF[j] > unknown_index_ajun:
                        index_FF_ajun = index_FF[j]
                        break
                if (index_FF.index(index_FF_ajun) > 0):
                    for k in range(0, len(index_QT)):
                        if index_QT[k] < index_FF[j] and index_QT[k] > index_FF[j - 1]:
                            unknown_index_ajun = -1
                            flag = 1
                            break
                    if flag == 0:
                        unknown_index = unknown_index_ajun
                        unknown_index_ajun = -1

                else:
                    if index_QT[0] < index_FF[0]:
                        unknown_index_ajun = -1
                    else:
                        unknown_index = unknown_index_ajun
                        unknown_index_ajun = -1

            if (len(index_FF) >= 3 and len(index_QT) >= 2):

                # Type 1 (subtraction)
                # Rekha has few books. Shyam gave her 6 books. Now she has 12 books. How many books did Rekha have earlier?
                if index_FF[0] > unknown_index:
                    qt2 = getEnglishNumbers(num_list[0])
                    qt3 = getEnglishNumbers(num_list[1])
                    unknown = qt3 - qt2
                    file_output.write(identifier + " " + "x=" + str(qt3) + "-" + str(qt2) + " x=" + str(unknown) + '\n')

                # Type 2 (subtraction)
                # Ali has 9 bags. He sold 3 bags. How many bag does he now have?
                # Type 7 (subtraction)
                # Radha has 7 cars in all. She has 5 red cars and remaining blue cars. How many blue cars does she have?
                elif index_FF[0] > index_QT[0] and index_FF[1] > index_QT[1] and unknown_index > index_QT[
                    0] and unknown_index > index_QT[1]:
                    qt1 = getEnglishNumbers(num_list[0])
                    qt2 = getEnglishNumbers(num_list[1])
                    unknown = qt1 - qt2
                    file_output.write(identifier + " " + "x=" + str(qt1) + "-" + str(qt2) + " x=" + str(unknown) + '\n')

                # Type 8 (subtraction)
                # Lata has 23 pearls. She gave few of them to Asha. Now she has 16 pearls. How many pearls did she give to Asha?
                # Type 9 (subtraction)
                # Sam has 40 radios. He gets few more radios. Now he has 73 radios. How many radios did he get?


                elif index_FF[0] > index_QT[0] and index_FF[1] > unknown_index and index_FF[1] < index_QT[
                    1] and unknown_index > index_QT[0] and unknown_index < index_QT[1]:
                    qt1 = getEnglishNumbers(num_list[0])
                    qt3 = getEnglishNumbers(num_list[1])
                    for j in range(0, len(index_VB)):
                        if index_VB[j] > unknown_index and index_VB[j] < index_FF[1]:
                            verb = verb_list[j]
                            if verb in positive_verbs:
                                wp_type = "positive"
                            elif verb in negative_verbs:
                                wp_type = "negative"
                            else:
                                wp_type = "unknown"

                    if wp_type == "negative":
                        unknown = qt1 - qt3
                        file_output.write(
                            identifier + " " + "x=" + str(qt1) + "-" + str(qt3) + " x=" + str(unknown) + '\n')
                    elif wp_type == "positive":
                        unknown = qt3 - qt1
                        file_output.write(
                            identifier + " " + "x=" + str(qt3) + "-" + str(qt1) + " x=" + str(unknown) + '\n')
                    else:
                        file_output.write(identifier + " " + "Unknown verb type" + '\n')

                else:
                    print(identifier + " " + "Invalid subtraction1 type")

            elif (len(index_FF) >= 2 and len(index_QT) >= 2):

                # Type 5 (subtraction)
                # Jordan has 3 cars. How  many more cars he needs to buy to have 12 cars?
                if index_FF[0] > index_QT[0] and unknown_index < index_QT[1] and unknown_index > index_QT[0]:
                    qt1 = getEnglishNumbers(num_list[0])
                    qt3 = getEnglishNumbers(num_list[1])
                    unknown = qt3 - qt1
                    file_output.write(identifier + " " + "x=" + str(qt3) + "-" + str(qt1) + " x=" + str(unknown) + '\n')
                else:
                    file_output.write(identifier + " " + "Invalid subtraction2 Type" + '\n')

            else:

                file_output.write(identifier + " " + "Invalid subtraction2 Type" + '\n')
        else:
            file_output.write(identifier + " " + "Invalid Type" + '\n')


