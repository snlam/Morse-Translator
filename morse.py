import csv

import nltk
import textblob

from textblob import TextBlob
from textblob import Word

from nltk.corpus import names  # see the note on installing corpora
# do dir(names) to see functions it has. names.raw(), names.readme()

import wordfreq
from wordfreq import word_frequency

d = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '10': '-----'}

def csv_to_txt():
    csv_file = input('Enter the name of your input file: ')
    txt_file = input('Enter the name of your output file: ')
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()

def readcsv( csv_file_name ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

#
# write_to_csv shows how to write that format from a list of rows...
#
def write_to_csv( list_of_rows, filename ):
    try:
        csvfile = open( filename, "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        count = 0
        for row in list_of_rows:
            count += 1
            filewriter.writerow(row ) 
            # filewriter.writerow( {row + ":" + str(list_of_rows[row])} ) # must be treated as list because csv returns a list
        csvfile.close()
    except:
        print("File", filename, "could not be opened for writing...")

lolita = readcsv("lolita copy.csv")
text = '' # the string version of the csv file
for row in lolita:
    for word in row:
        text += word

tb = TextBlob('Lolita, light of my life, fire of my loins• My sin, my soul• Lo_Lee_Ta: the tip of the tongue taking a Trip of three steps down the palate to tap, at three, on the teeth• Lo• Lee• Ta• She was lo, plain lo, in the morning, standing four feet ten in one sock• She was Lola in slacks• She was Dolly at school• She was Dolores on the dotted line• But in my arms she was always lolita• Did she have a precursor? She did, indeed she did• In point of fact, there might have been no Lolita at all had I not loved, one summer, an initial girl_child• In a princedom by the sea• Oh when? About as many years before Lolita was born as my age was that summer• You can always count on a murderer for a Fancy prose style• Ladies and gentlemen of the jury, exhibit number one is what the seraphs, the misinformed, simple, noble_winged seraphs, envied• Look at this tangle of thorns• ')
lolitawords = tb.words

def frommorse2(text): # use if given morse code that's not separated by spaces
    output = ''
    f = tomorse(text).replace(' ', '').replace('/', '') # now the text converted to morse has no spaces
    # print(f)
    for i in range(len(f)):
        if f[i] != '/':
            k = frommorse(f[i] + ' ') # right now, these are just giving the frequencies of each possible letter since morse code quintuplets still count as 1 letter
            l = frommorse(f[i:i+2] + ' ')
            m = frommorse(f[i:i+3] + ' ')
            n = frommorse(f[i:i+4] + ' ')
            o = frommorse(f[i:i+5] + ' ')
            # print(k)
            # print(l)
            # print(m)
            # print(n)
            # print(o)
            g = [word_frequency(k, 'en'), word_frequency(l, 'en'), word_frequency(m,'en'), word_frequency(n, 'en'), word_frequency(o, 'en')]
            if max(g) == g[0]:
                k = k.replace(' ', '')
                output += k
            elif max(g) == g[1]:
                l = l.replace(' ', '')
                output += l
            elif max(g) == g[2]:
                m = m.replace(' ', '')
                output += m
            elif max(g) == g[3]:
                n = n.replace(' ', '')
                output += n
            elif max(g) == g[4]:
                o = o.replace(' ', '')
                output += o
            # print(max(g))
        else:
            output += ' '
    return output

def frommorse(text): # use if given morse code that is separated by spaces
    output = ''
    words = []
    words2 = []
    newindex = 0
    textcopy = text
    for x in text:
        if text.count(' ') >= 1: # if you're translating a morse code snippet where words are separated by spaces
            if x == ' ': # if given morse code where words are separated by spaces
                if textcopy.count(' ') >= 1:
                    newword = textcopy[0: textcopy.find(' ')]
                    if newword.startswith('/'):
                        words += ['/']
                        newword = textcopy[1: textcopy.find(' ')]
                    words += [newword]
                    newindex = textcopy.find(' ') + 1 
                    textcopy = textcopy[newindex: ]
            elif ' ' not in textcopy: # if there are no more spaces
                words += [textcopy]
    for i in range(len(words)):
        if words[i] == '.-':
            words[i] = 'a'
        elif words[i] == '-...':
            words[i] = 'b'
        elif words[i] == '-.-.':
            words[i] = 'c'
        elif words[i] == '-..':
            words[i] = 'd'
        elif words[i] == '.':
            words[i] = 'e'
        elif words[i] == '..-.':
            words[i] = 'f'
        elif words[i] == '--.':
            words[i] = 'g'
        elif words[i] == '....':
            words[i] = 'h'
        elif words[i] == '..':
            words[i] = 'i'
        elif words[i] == '.---':
            words[i] = 'j'
        elif words[i] == '-.-':
            words[i] = 'k'
        elif words[i] == '.-..':
            words[i] = 'l'
        elif words[i] == '--':
            words[i] = 'm'
        elif words[i] == '-.':
            words[i] = 'n'
        elif words[i] == '---':
            words[i] = 'o'
        elif words[i] == '.--.':
            words[i] = 'p'
        elif words[i] == '--.-':
            words[i] = 'q'
        elif words[i] == '.-.':
            words[i] = 'r'
        elif words[i] == '...':
            words[i] = 's'
        elif words[i] == '-':
            words[i] = 't'
        elif words[i] == '..-':
            words[i] = 'u'
        elif words[i] == '...-':
            words[i] = 'v'
        elif words[i] == '.--':
            words[i] = 'w'
        elif words[i] == '-..-':
            words[i] = 'x'
        elif words[i] == '-.--':
            words[i] = 'y'
        elif words[i] == '--..':
            words[i] = 'z'
        elif words[i] == '.----':
            words[i] = '1'
        elif words[i] == '..---':
            words[i] = '2'
        elif words[i] == '...--':
            words[i] = '3'
        elif words[i] == '....-':
            words[i] = '4'
        elif words[i] == '.....':
            words[i] = '5'
        elif words[i] == '-....':
            words[i] = '6'
        elif words[i] == '--...':
            words[i] = '7'
        elif words[i] == '---..':
            words[i] = '8'
        elif words[i] == '----.':
            words[i] = '9'
        elif words[i] == '-----':
            words[i] = '10'
        elif words[i] == '/':
            words[i] = ' '
        elif words[i] == ',' or words[i] == '?' or words[i] == '!' or words[i] == '"':
            words[i] = words[i]
        output += words[i]

    final2 = ''
    for word in words:
        final2 += word
    final2 = final2.split(' ')

    L = names.raw()
    M = L.split("\n")
    lowerM = [x.lower() for x in M]
    for i in range(len(final2)):
        if i == 0:
            final2[i] = final2[i].title() # capitalize the first letter of the text
        if i >= 1:
            if final2[i-1].endswith('•') or final2[i-1].endswith('?') or final2[i-1].endswith('!'):
                final2[i] = final2[i].title() 
            elif final2[i][-1] == '•' and final2[i] in lowerM:
                final2[i] = final2[i].title()[0:final2[i].find('•')] # words[i+1] is morse code
        if final2[i] == 'i' or final2[i] == 'lo' or final2[i] in lowerM:
            final2[i] = final2[i].title()
    final = ''
    for word in final2:
        final = final + word + ' '
    return final


# replaces periods with dots and dashes to underscores to avoid confusing the script when it translates morse back to english
def tomorse(text):
    output = ''
    for char in text:
        if char == ',' or char == '?' or char == '!' or char == ':' or char == ';':
            char = char + ' '
        elif char == "'" or char == '"':
            char = char + ' '
        elif char.lower() == 'a':
            char = '.- '
        elif char.lower() == 'b':
            char = '-... '
        elif char.lower() == 'c':
            char = '-.-. '
        elif char.lower() == 'd':
            char = '-.. '
        elif char.lower() == 'e':
            char = '. '
        elif char.lower() == 'f':
            char = '..-. '
        elif char.lower() == 'g':
            char = '--. '
        elif char.lower() == 'h':
            char = '.... '
        elif char.lower() == 'i':
            char = '.. '
        elif char.lower() == 'j':
            char = '.--- '
        elif char.lower() == 'k':
            char = '-.- '
        elif char.lower() == 'l':
            char = '.-.. '
        elif char.lower() == 'm':
            char = '-- '
        elif char.lower() == 'n':
            char = '-. '
        elif char.lower() == 'o':
            char = '--- '
        elif char.lower() == 'p':
            char = '.--. '
        elif char.lower() == 'q':
            char = '--.- '
        elif char.lower() == 'r':
            char = '.-. '
        elif char.lower() == 's':
            char = '... '
        elif char.lower() == 't':
            char = '- '
        elif char.lower() == 'u':
            char = '..- '
        elif char.lower() == 'v':
            char = '...- '
        elif char.lower() == 'w':
            char = '.-- '
        elif char.lower() == 'x':
            char = '-..- '
        elif char.lower() == 'y':
            char = '-.-- '
        elif char.lower() == 'z':
            char = '--.. '
        elif char == '1':
            char = '.---- '
        elif char == '2':
            char = '..--- '
        elif char == '3':
            char = '...-- '
        elif char == '4':
            char = '....- '
        elif char == '5':
            char = '..... '
        elif char == '6':
            char = '-.... '
        elif char == '7':
            char = '--... '
        elif char == '8':
            char = '---.. '
        elif char == '9':
            char = '----. '
        elif char == '10':
            char = '----- '
        elif char == ' ':
            char = '/'
        elif char == '.':
            char = '• '
        elif char == '-':
            char = '_ '
        output += char
    return output