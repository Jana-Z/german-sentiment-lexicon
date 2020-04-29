# German sentiment lexicon
A lexicon to be used for German emotion detection

## Table of Contents
- General info
- File structure / Documentation
- Ressources
- Technologies
- Setup
- Todo

## General info
The lexicon is compossed of word assosociated with (number of samples):
- love / liebe
- disgust / ekel
- joy / freude
- fright / angst
- anger / wut
- contempt / verachtung
- grief / trauer
- surprise / überraschung
These emotions are roughly based on [Paul Ekman's theory of emotions](https://en.wikipedia.org/wiki/Paul_Ekman#Emotions_as_universal_categories).

## File structure / Documentation

### Emotions
Contains 8 txt files.
Each labeled according to one feeling: ('ekel', 'furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude', 'liebe')
After each word there is a score of how often the word appeared as a assosiaction.  
Values are not scaled!  
Duplicates are possible  

Emotion | love | disgust | joy | fright | anger | contempt | grief | surprise
--- | --- | --- | --- | --- | --- | --- |--- | ---
Samples | 904 | 510 | 1261 | 1052 | 990 | 2567 | 1243 | 995


## Ressources
### Emotions
The data was mined from four German online dictionaries.
Each dictionary got a reliability score.
The dictionaries were:
- [dwds](https://www.dwds.de/) (0.5)
- [duden](https://www.duden.de/) (1.0)
- [synonyme_de](https://www.synonyme.de/)(1.0)
- [wordassosiactions](https://wordassociations.net/de/) (0.8)

The sites mined for words assosiacted with this feeling. The reliability scores of each ressource, where a word was found were added up.

This step was repeated for the most important assosiactions.

For every emotion (except for love) feelings from [Roman Klinger and Surayya Samat Suliya](https://bitbucket.org/rklinger/german-emotion-dictionary/src/master/) were added with a score of 1.0.

### Stop words
The stop words are a stemmed combination of the following lists of german stop words:
- [solariz](https://github.com/solariz/german_stopwords/blob/master/german_stopwords_full.txt)
- [stopwords-iso](https://github.com/stopwords-iso/stopwords-de/blob/master/stopwords-de.txt)
- [snowball](https://snowballstem.org/algorithms/german/stop.txt)
- [Roman Klinger and Surayya Samat Suliya](https://bitbucket.org/rklinger/german-emotion-dictionary/src/master/)

### Stemmming
The general idea for the algorithm was taken from [Snowball](https://snowballstem.org/algorithms/german/stemmer.html)

## Technologies
Project is created with:
- Python 3.7.7
- [BeautifulSoup 4.9.0](http://www.crummy.com/software/BeautifulSoup/bs4/)
- [Selenium 3.141.0](https://github.com/SeleniumHQ/selenium/)

## Setup
Download or clone this repository.

An (easy) function on how to read the CSV file can be found at ```./bin/manage_files.py``` (def load_csv_file) 

## Todo  

- [x] Add words from comparing emotions on dwds
- [x] Add stemmed and regularized versions.
- [ ] Add sample project.
- [x] Add stop words
- [ ] remove stop words from emotions