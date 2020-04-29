import re

def stem(word):
    # algorithm from https://snowballstem.org/algorithms/german/stemmer.html
    word = word.strip()
    word = re.sub(r'ß', 'ss', word)
    word = word.lower()

    r_1 = _define_regions(word)
    if len(word) - len(r_1) < 3:
        r_1 = word[2:]
    r_2 = _define_regions(r_1)

    suffixes = {
        'a': {'em', 'ern', 'er'},
        'b': {'e', 'en', 'es'},
        'c': {'bs', 'ds', 'fs', 'gs', 'hs', 'ks', 'ls', 'ms', 'ns', 'rs', 'ts'}
    }

    if len(word) > 3:
        for category, suffix in suffixes.items():
            for s in suffix:
                if s in word[-len(s):] and word[-len(s):] in r_1:
                    if category == 'a' or category == 'b':
                        word = word[:-len(s)]
                        r_1 = r_1[:-len(s)]
                        r_2 = r_2[:-len(s)]
                        break
                    if category == 'b':
                        if len(word) > 4:
                            if word[-4:] == 'niss':
                                word = word[:-1]
                                r_1 = r_1[:-1]
                                r_2 = r_2[:-1]
                            break


    suffixes = {
        'a': {'en', 'er', 'est'},
        'b': {'bst', 'dst', 'fst', 'gst', 'hst', 'kst', 'lst', 'mst', 'nst', 'tst'}
    }

    if len(word) > 3:
        for category, suffix in suffixes.items():
            for s in suffix:
                if s in word[-len(s):] and word[-len(s):] in r_1:
                    if category == 'a':
                        word = word[:-len(s)]
                        r_1 = r_1[:-len(s)]
                        r_2 = r_2[:-len(s)]
                        break
                    if category == 'b' and len(word) > 5:
                        word = word[:-len(s)+1]
                        r_1 = r_1[:-len(s)+1]
                        r_2 = r_2[:-len(s)+1]
                        break


    suffixes = {
        'a': {'end', 'ung'},
        'b': {'ig', 'ik', 'isch'},
        'c': {'lich', 'heit'},
        'd': {'keit'}    
    }

    for category, suffix in suffixes.items():
        for s in suffix:
            if s in word[-len(s):] and word[-len(s):] in r_2:
                if category == 'a':
                    word = word[:-len(s)]
                    r_1 = r_1[:-len(s)]
                    r_2 = r_2[:-len(s)]
                    if r_2[-2:] == 'ig' and word[-3] != 'e':
                        word = word[:-2]
                        r_1 = r_1[:-2]
                        r_2 = r_2[:-2]
                    break
                if category == 'b' and word[-len(s)-1] != 'e':
                    word = word[:-len(s)]
                    r_1 = r_1[:-len(s)]
                    r_2 = r_2[:-len(s)]
                    break
                if category == 'c':
                    word = word[:-len(s)]
                    r_1 = r_1[:-len(s)]
                    r_2 = r_2[:-len(s)]
                    if r_1[-2:] in {'er', 'en'}:
                        word = word[:-2]
                        r_1 = r_1[:-2]
                        r_2 = r_2[:-2]
                    break
                if category == 'd':
                    word = word[:-len(s)]
                    r_1 = r_1[:-len(s)]
                    r_2 = r_2[:-len(s)]
                    if r_2[-4:] == 'lich':
                        word = word[:-4]
                        r_1 = r_1[:-4]
                        r_2 = r_2[:-4]
                        break
                    if r_2[-2:] == 'ig':
                        word = word[:-2]
                        r_1 = r_1[:-2]
                        r_2 = r_2[:-2]
                break

    word = re.sub(r'ä', 'a', word)
    word = re.sub(r'ö', 'o', word)
    word = re.sub(r'ü', 'u', word)

    return word

def _define_regions(word):
    vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö', 'ü'}
    if not word: return ''
    if word[0] in vowels:
        i = 1
        while i < len(word):
            if word[i] not in vowels:
                return word[i+1:]
            i += 1
    else: 
        i = 1
        found_vowel = False
        while i < len(word):
            if word[i] in vowels:
                found_vowel = True
            if found_vowel == True and word[i] not in vowels:
                return word[i+1:]
            i += 1
    return ''
