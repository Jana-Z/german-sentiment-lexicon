import os
import sys
import csv

from flesch_kincaid_readability import *
from fundementals import convert_umlaute, \
    count_words, capitalize

def add_local_emotions(dirpath_src, dirpath_dst)
    emotionlist = ['furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude']

    for emotion in emotionlist:
        add_file_to_csv(
            os.path.join(dirpath_src, emotion + '.txt'),
            os.path.join(dirpath_dst, emotion + '.txt'),
        )

def add_to_csv(filepath, dict_to_be_saved):
    # save as csv
    # add duplicates up:
    if os.path.isfile(filepath):
        with open(filepath,'r', newline = '') as f:
            reader = csv.reader(f, delimiter=',')
            content = [l.strip() for l in reader] if not reader else []

        content = dict(content) if not content else {}
        for addition, score in dict_to_be_saved.items():
            additon = addition.strip()
            if addition not in content:
                content[addition] = score
            else:
                content[addition] = float(content[addition]) + float(score)

        with open(filepath, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in content.items():
                writer.writerow(list(row))
    else:
        print(f'{filepath} is not a path to a file')
        return None

def load_csv_file(filepath, threshold=None):
    # comma seperated
    if os.path.isfile(filepath):
        with open(filepath, 'r', newline = '') as f:                                                                                          
            reader = csv.reader(f, delimiter=',')
            if not threshold:
                return dict([key, float(value)]
                    for key, value in dict(reader).items())
            else:
                return dict([key, float(value)]
                    for key, value in dict(reader).items()  
                    if float(value) > threshold)
    else:
        print(f'{filepath} is not a path to a file')
        return None

def add_file_to_csv(filepath_src, filepath_dst):
    print(return_file_by_line(filepath_src))
    content_new = dict.fromkeys(
        return_file_by_line(filepath_src),
        1.0
    )
    add_to_csv(filepath_dst, content_new)

def return_file_by_line(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            content = f.readlines()
        return [c.strip() for c in content]
    else:
        print(f'{filepath} is not a path to a file')
        return None


# development functions
def clean_all_files_in_dir(dirpath):
    all_files = find_all_files_in_dir(dirpath)
    for filepath in all_files:
        clean_file(filepath)

def clean_file(filepath):
    # deletes duplicates and sorts in alphabetical order
    with open(filepath, 'r') as f:
        file_dirty = [line.strip() for line in f.readlines()]
    if not file_dirty:
        print(f'{filepath} was an empty file -> nothing to clean')
    else:
        file_clean = set(file_dirty)
        file_clean = list(file_clean)
        file_clean.sort()
        with open(filepath, 'w') as f:
            f.write("\n".join(file_clean))
        f.close()
    f.close()

def find_all_files_in_dir(dirpath):
    # only works with txt files
    if os.path.isdir(dirpath):
        all_files = []
        for file in os.listdir(dirpath):
            if file.endswith(".txt"):
                all_files.append(os.path.join(dirpath, file))
        return all_files
    else:
        print(f'{dirpath} is no path to a dir')
        return None
