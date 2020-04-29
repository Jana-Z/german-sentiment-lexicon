import os
import csv

from manage_files import *
from stemming import stem

EMOTIONLIST = ['ekel', 'furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude', 'liebe']
PATH_STOP_WORDS = '../data/stopwords.txt'
DST_DIR: '../data/emotions/raw/'

def main(dst_dir, regulize=True, unique_words=True, stem_words=True):
    emotionlist = ['ekel', 'furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude', 'liebe']

    path_stop_words = '../data/stopwords.txt'

    
    remove_stop_words(dst_dir, EMOTIONLIST)
    if unique_words: handle_dupilcates(dst_dir, emotionlist)
    if regulize: regularize_data(dst_dir, EMOTIONLIST)
    if stem_words: stem_emotions(dir_no_duplicates, emotionlist)

def cleanse_stopwords():
    stem_words(PATH_STOP_WORDS)
    remove_duplicates(PATH_STOP_WORDS)

def remove_stop_words(filepath_stop_words, dirpath, emotionlist):
    with open(filepath_stop_words, 'r') as f:
        stop_words = f.readlines()
    stop_words = set([w.strip() for w in stop_words])
    for emotion in emotionlist:
        filepath = os.path.join(dirpath, emotion + '.txt')
        assosiacations = load_csv_file(filepath)
        better_assosiacations = {key:val for key, val in assosiacations.items() if key not in stop_words}
        write_csv_file(filepath, better_assosiacations)

def remove_duplicates(filepath):
    with open(filepath, 'r') as f:
        words = f.readlines()
    words = set([w.strip() for w in words])
    words = sorted(list(words))
    with open(filepath, 'w') as f:
        f.writelines("%s\n" % w for w in words)

def regularize_data(dirpath, emotionlist):
    for emotion in emotionlist:
        filepath = os.path.join(dirpath, emotion + '.txt')
        remove_low_scores(filepath)
        scale_csv(filepath)

def stem_words(filepath):
    with open(filepath, 'r') as f:
        words = f.readlines()
    with open(filepath, 'w') as f:
        f.writelines("%s\n" % stem(w) for w in words)


def stem_emotions(dirpath, emotionlist):
    for emotion in emotionlist:
        filepath = os.path.join(dirpath, emotion + '.txt')
        words = load_csv_file(filepath)
        stemmed_words = {}
        for word, score in words.items():
            stemmed_word = stem(word)
            if  stemmed_word in stemmed_words:
                stemmed_words[stemmed_word] = stemmed_words[stemmed_word] \
                if stemmed_words[stemmed_word] > score else score
            else:
                stemmed_words[stemmed_word] = score
        write_csv_file(filepath, stemmed_words)   

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
            if word not in data_flipped: 
                data_flipped[word] = [[emotion, score]] 
            else: 
                data_flipped[word].append([emotion, score])
                duplicates.add(word)

    # go through duplicates
    for duplicate in duplicates:
        occurences = data_flipped[duplicate]
        scores = [entry[1] for entry in occurences]
        max_value = max(scores)
        strongest = scores.index(max_value)
        data_flipped[duplicate] = [(strongest, max_value)]
    
    print(duplicates)

    data = {}
    # flip data back
    for word, value in data_flipped.items():
        emotion = value[0][0]
        score = value[0][1]
        if emotion not in data:
            data[emotion] = {
                word: score
            }
        else:
            data[emotion][word] = score

    for emotion in emotionlist:
        write_csv_file(
            os.path.join(dirpath, emotion + '.txt'),
            data[emotion]
        )

if __name__ == '__main__':
    main()