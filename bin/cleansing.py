import os
import csv

from manage_files import *

def main():
    emotionlist = ['ekel', 'furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude', 'liebe']
    dirpath = '../data/emotions'

    for emotion in emotionlist:
        filepath = os.path.join()
        remove_low_scores(filepath)
        scale_csv(filepath)

def scale_csv(filepath):
    if os.path.isfile(filepath):
        with open(filepath,'r', newline = '') as f:
            reader = csv.reader(f, delimiter=',')
            content = [l for l in reader] if reader else []

        content = dict([word, float(score)]
            for word, score in dict(content).items()) \
            if content else {}

        max_score = float(max(content.values()))
        
        for word, score in content.items():
            content[word] = score / max_score

        print(float(max(content.values())))

        with open(filepath, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in content.items():
                writer.writerow(list(row))
    else:
        print(f'{filepath} is not a path to a file')
        return None        

def remove_low_scores(filepath, threshhold=0.5):
    if os.path.isfile(filepath):
        with open(filepath,'r', newline = '') as f:
            reader = csv.reader(f, delimiter=',')
            content = [l for l in reader] if reader else []

        content = dict([word, float(score)]
            for word, score in dict(content).items()
            if float(score) > threshhold) \
            if content else {}

        write_csv_file(filepath, content)
    else:
        print(f'{filepath} is not a path to a file')
        return None

def handle_dupilcates(dirpath, emotionlist):
    # deletes duplicates in file where score is lower
    # load data flipped
    data_flipped = {}
    duplicates = set()
    for emotion in emotionlist:
        filepath = os.path.join(dirpath, emotion + '.txt')
        for word, score in load_csv_file(filepath).items():
            if value not in flipped: 
                data_flipped[word] = [(emotion, score)] 
            else: 
                data_flipped[word].append((emotion, score))
                duplicates.add(word)

    # go through duplicates
    for duplicate in duplicates:
        occurences = data_flipped[duplicate]
        scores = [entry[1] for entry in occurences])
        max_value = max(scores)
        strongest = scores.index(max_value)
        data_flipped = [(occurences[strongest], max_value)]
    
    data = dict.fromkeys(emotionlist)
    # flip data back
    for word, value in data_flipped.items():
        emotion = value[0]
        score = value[1]
        if emotion not in data:
            

    for emotion in emotionlist:
        


def stemm_data():
    pass

def remove_stop_words():
    pass

if __name__ == '__main__':
    main()