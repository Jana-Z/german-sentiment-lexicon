import re

def count_words(text):
    words = re.findall(r'\w+', text)
    return len(words)

def convert_umlaute(string):
    string = string.replace( "ä", "ae" )
    string = string.replace( "ö", "oe" )
    string = string.replace( "ü", "ue" )
    string = string.replace( "Ä", "Ae" )
    string = string.replace( "Ö", "Oe" )
    string = string.replace( "Ü", "Ue" )
    string = string.replace( "ß", "ss" )
    return string

def capitalize(string):
    if not string:
        return None
    if len(string) < 2:
        return string.upper()
    return string[0].upper() + string[1:].lower()