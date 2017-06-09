import sys
import os
from functools import reduce
from math import exp

#function that reads the input files:
def read_files(candidate_path, reference_path):

    reference = []

    if os.path.isdir(reference_path):
        for root, dir, files in os.walk(reference_path):
            for file in files:
                fr1 = open(os.path.join(root, file), 'r', encoding="utf8")
                reference.append(fr1.readlines())
                fr1.close()
    else:
        fr1 = open(reference_path, 'r', encoding="utf8")
        reference.append(fr1.readlines())
        fr1.close()

    fr2 = open(candidate_path, 'r', encoding="utf8")
    candidate = fr2.readlines()
    fr2.close()

    return(candidate, reference)

# function that calculate BLEU score
def calculate_bleu(candidate, reference):

    precise = []
    for i in range(1, 5):
        precision = calculate_ngram(candidate, reference, i)
        precise.append(precision)
    brevity = calculate_brevity(candidate, reference)
    bleu = calculate_gm(precise) * brevity
    return(bleu)

#function that calculate Geometric Mean
def calculate_gm(pr):

    return((reduce((lambda x, y: x*y), pr))**(1.0/len(pr)))

# function that calculate N-Gram Precision
def calculate_ngram(candidate, references, n):

    count = 0
    clip = 0

    for i in range(len(candidate)):
        ref_counts = []
        ref_len = []
        for reference in references:
            sentence = reference[i]
            dict_ngram = {}
            words = sentence.strip().split()
            ref_len.append(len(words))
            loop_end = len(words) - n +1
            for j in range(loop_end):
                ng_word = ' '.join(words[j:j+n]).lower()
                if ng_word in dict_ngram:
                    dict_ngram[ng_word] += 1
                else:
                    dict_ngram[ng_word] = 1
            ref_counts.append(dict_ngram)

        sentence = candidate[i]
        dict_cand = {}
        words = sentence.strip().split()
        loop_end = len(words)-n+1
        for j in range(loop_end):
            cand_word = ' '.join(words[j:j+n]).lower()
            if cand_word not in dict_cand:
                dict_cand[cand_word] = 1
            else:
                dict_cand[cand_word] += 1
        clip += clipped_count(dict_cand, ref_counts)
        count += loop_end
    if clip == 0:
        pr = 0
    else:
        pr = float(clip / count)
    return(pr)

#function to find clipped length of each word in sentence of candidate with corresponding reference sentence
def clipped_count(dict_cand, ref_counts):
    cnt = 0
    for k in dict_cand.keys():
        value = dict_cand[k]
        max_val = 0
        for ref in ref_counts:
            if k in ref.keys():
                max_val = max(max_val, ref[k])
        value = min(value, max_val)
        cnt += value
    return  cnt

#function to find(brevity penalty (length of sentence difference candidate to reference)
def calculate_brevity(candidate, references):
    bp_r = 0
    bp_c = 0
    for i in range(len(candidate)):
        ref_len = []
        for reference in references:
            sentence = reference[i]
            words = sentence.strip().split()
            ref_len.append(len(words))
        sentence = candidate[i]
        words = sentence.strip().split()
        bp_r += find_best_match(ref_len, len(words))
        bp_c += len(words)

    if bp_c >= bp_r:
        bp = 1
    else:
        bp = exp(1-(float(bp_r/bp_c)))
    return(bp)

#function finds the best matching length of reference among various reference of a sentence
def find_best_match(ref_len, len_words):

    diff = abs(len_words - ref_len[0])
    best = ref_len[0]
    for ref in ref_len:
        if abs(len_words - ref) < diff:
            diff = abs(len_words - ref)
            best = ref
    return(best)



def main():

    # for test run use debug = True else False
    debug = True

    if debug != True:
        if len(sys.argv) != 3:
            print("Error: Please enter both the Candidate File as well as reference File")
            sys.exit(1)

        candidate_file = sys.argv[1]
        reference_file = sys.argv[2]
    else:
        candidate_file = 'candidate-2.txt'
        reference_file = 'reference-2.txt'

    candidate , reference = read_files(candidate_file, reference_file)
    bleu = round(calculate_bleu(candidate, reference),12)
    if debug == True:
        print(bleu)
    else:
        fw = open('bleu_out.txt', 'w')
        fw.write(str(bleu))
        fw.close()

# calling main()
main()