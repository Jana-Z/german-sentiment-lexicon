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

## File structure / Documentation

### Emotions
Contains 8 txt files.
Each labeled according to one feeling: ('ekel', 'furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude', 'liebe')
After each word there is a score of how often the word appeared as a assosiaction.
Values are not scaled!
Duplicates are possible


## Ressources
The data was mined from four German online dictionaries.
Each dictionary got a reliability score.
The dictionaries were:
- (dwds)[https://www.dwds.de/] (0.5)
- (duden)[https://www.duden.de/] (1.0)
- (synonyme_de)[https://www.synonyme.de/] (1.0)
- (wordassosiactions)[https://wordassociations.net/de/] (0.8)

The sites mined for words assosiacted with this feeling. The reliability scores of each ressource, where a word was found were added up.

This step was repeated for the most important assosiactions.

For every emotion (but love and conrempt) feelings from (Roman Klinger and Surayya Samat Suliya)[https://bitbucket.org/rklinger/german-emotion-dictionary/src/master/] were added with a score of 1.0.

## Technologies
Project is created with:
- Python3
- BeautifulSoup
- Selenium

## Setup
Download or clone this repository.

## Todo
- Add words from comparing emotions on dwds
- Add stemmed and regularized versions.
- Add sample project.
- Add stop words (remove stop words from emotions)