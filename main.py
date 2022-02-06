#What do I want to do..
# Find best starting word
# How
# Iterate through each word in huge dictionary
# Try 10000 times on unique words
# What is strategy
# Hard Mode
# Try most popular letters
# First find dictionary 

from mimetypes import guess_extension
from re import L, S
import string
from tokenize import String
from tracemalloc import start
from turtle import pos, st
import copy
from jinja2 import TemplateNotFound
from torch import le
import threading
import time
from timeit import default_timer as timer
import random
'''
class Node(): 
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    def __init__(self, word=[None,None,None,None,None], parent=None) -> None:
        self.word = word
        if None not in word:
            self.first = None
            self.second = None
            self.third = None
            self.fourth = None
            self.fifth = None
            self.children = None
        else:
            self.first={key: None for key in self.letters}
            self.second={key: None for key in self.letters}
            self.third={key: None for key in self.letters}
            self.fourth={key: None for key in self.letters}
            self.fifth={key: None for key in self.letters}
            self.children=[self.first, self.second, self.third, self.fourth, self.fifth]
        self.parent = parent
    
    def getLength(self) -> int:
        return len(self.word)

    def getEachChild(self) -> list:
        return self.children
    
    def getEachChildNumberedAndSelf(self):
        toRet = []
        for i,child in enumerate(self.children):
            toRet.append([self, i, child])
        return toRet

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.word)+"\n"
        for child in self.children:
            for key in child:
                if child[key] != None:
                    ret += child[key].__str__(level+1)
                else:
                    ret += "\t"*level+"None\n"
        return ret

    def __repr__(self):
        return '<tree Node representation>'

    #letters = ['a','b','c']#,'d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


 Too many iterations, billions of nodes (185,646,500,000)
def buildGraph():
    root = Node()
    if None not in root.word:
        return []
    visited= []
    stack = root.getEachChildNumberedAndSelf()
    while stack:
        print(len(stack))
        pair = stack.pop()
        currParent = pair[0]
        position = pair[1]
        childDict = pair[2]
        tempNode = None
        for key in childDict:
            tempWord = copy.copy(currParent.word)
            tempWord[position] = key
            tempNode = Node(word=tempWord, parent=currParent)
            childDict[key] = tempNode
            if None in tempWord:
                visited.append(tempNode)
                stack.extend(tempNode.getEachChildNumberedAndSelf())  
    return root
    '''

"""
from https://github.com/charlesreid1/five-letter-words/blob/master/get_words.py
get_words.py
Utility method to load the SBG words
and retun them as a list of strings.
"""
def getWords():
    # Load the file.
    with open('sgb-words.txt','r') as f:
        ## This includes \n at the end of each line:
        #words = f.readlines()
    
        # This drops the \n at the end of each line:
        words = f.read().splitlines()

    return words

def buildLetterDict(words):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    letterDicts = [{key: [] for key in letters},{key: [] for key in letters},{key: [] for key in letters},{key: [] for key in letters},{key: [] for key in letters}]
    for word in words:
        for i,letter in enumerate(word):
            letterDicts[i][letter].append(word)
    return letterDicts

def checkGuess(guess, target, guessMatrix):
    guessMatrix[0].append(guess)
    for i,letter in enumerate(guess):
        if target[i] == letter:
            guessMatrix[1][i] = letter
        elif letter in target:
            guessMatrix[2].append([i,letter])
        elif letter not in guessMatrix[3]:
            guessMatrix[3].append(letter)
    return guessMatrix

def makeGuessList(words,guessMatrix,letterDicts):
    guessList = copy.copy(words)

    #If we know position of letter
    for i,letterFound in enumerate(guessMatrix[1]):
        if letterFound:
            guessList = [value for value in guessList if value in letterDicts[i][letterFound]]
    #print(guessMatrix[1], len(guessList))

    #remove where letter is in wrong spot or not in word
    for pair in guessMatrix[2]:
        guessList = [word for word in guessList if pair[1] in word and word[pair[0]] != pair[1]]
    #print(guessMatrix[2], len(guessList))

    #remove where letter is not in word
    for letter in guessMatrix[3]:
        guessList = [word for word in guessList if letter not in word]
    #print(guessMatrix[3], len(guessList))

    if len(guessList) == 0:
        return None

    return guessList

def guessWord(words, target, guessMatrix, letterDicts):
    guessList = makeGuessList(words,guessMatrix, letterDicts)
    #first look at confirmed letters and add all words with those confirmed letters
    #Prob freq dictionary where looking for number of non nones in confirmed letters

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    freqDict = {key: 0 for key in letters}
    for word in guessList:
        for letter in word:
            freqDict[letter] += 1

    bestGuessList = []
    for word in guessList:
        score = 0
        letters = []
        for letter in word:
            if letter not in letters:
                score += freqDict[letter]
            letters.append(letter)
        bestGuessList.append([score,word])
    bestGuessList.sort()
    return checkGuess(bestGuessList[-1][1],target,guessMatrix)
    

def thread(words, startingWords, letterDicts, attemptDict, x, startingWord, successDict, failureDict, guessingDict):
    attemptDict[startingWord] = 0
    successDict[startingWord] = 0
    failureDict[startingWord] = 0
    guessingDict[startingWord] = []
    results = [0,0]
    for n,target in enumerate(words):#[-2:-1]):
        #print("target", target)
        if startingWord != target:
            #print(n,"/",len(words),"|",x,"/",len(startingWords))
            guessMatrix = [[],[None,None,None,None,None],[],[]]
            guessMatrix = checkGuess(startingWord,target,guessMatrix)
            while len(guessMatrix[0]) < 6 and target not in guessMatrix[0]:
                guessMatrix = guessWord(words,target,guessMatrix,letterDicts)
                if guessMatrix == None:
                    print("failed")
                    quit()
            guessingDict[startingWord].append([guessMatrix[0],"-->",target])
            if target in guessMatrix[0]:
                #print("     good guess",guessMatrix[0])
                results[0] += 1
                attemptDict[startingWord] += len(guessMatrix[0])
                successDict[startingWord] += 1
            else:
                #print("     bad guess",guessMatrix[0])
                results[1] += 1
                failureDict[startingWord] += 1
    attemptDict[startingWord] = attemptDict[startingWord]/max(successDict[startingWord],1)

def thread2(words, startingWords, letterDicts, attemptDict, x, startingWord, successDict, failureDict, guessingDict, testDict):
    for x,target in enumerate(words):
        if startingWord != target:
            guessMatrix = [[],[None,None,None,None,None],[],[]]
            guessMatrix = checkGuess(startingWord,target,guessMatrix)
            guessList = makeGuessList(words,guessMatrix,letterDicts)
            if not guessList:
                print("error")
                return
            testDict[startingWord] += len(guessList)
        #print("Progress "+str((x+1)/len(words)*100)[0:4] +"%")
    testDict[startingWord] = testDict[startingWord]/len(words)

            
if __name__=="__main__":
    start = timer()
    words = getWords()
    '''
    freqDict = {}
    for word in words:
        freqDict[word] = 0
        seen = []
        for letter in ['e','a','r','o','t']:
            if letter in word and letter not in seen:
                freqDict[word] += 1
                seen.append(letter)
    for out in sorted(freqDict.items(), key=lambda item: item[1], reverse=True)[:100]:
        print(out)
    end = timer()
    print(end-start)
    if 1:
        quit(0)
        '''

    letterDicts = buildLetterDict(words)
    attemptDict = {}
    successDict = {}
    failureDict = {}
    guessingDict = {}
    myThreads = []
    k=10
    #startingWords = random.choices(words, k=10)
    #startingWords = copy.copy(words)
    startingWords = ['salet', 'irate']
    #startingWords = ['abort','actor','adore','after','alert','alter','aorta','arose','atone','avert','cater','crate','earth','eater','extra','forte','grate','great','hater','heart','irate','later','metro','opera','other','otter','outer','ovate','overt','ratio','react','retro','roast','route','stare','store','taker','tamer','taper','tarot','teary','tenor','terra','tower','trace','trade','tread','treat','trope','trove','voter','water','wrote']
    testDict =  {word: 0 for word in startingWords}
    for x,startingWord in enumerate(startingWords):
        print(str(x)+"/"+str(len(startingWords)))
        try:
            t = (threading.Thread(target=thread2, args=(words, startingWords, letterDicts, attemptDict, x, startingWord, successDict, failureDict, guessingDict, testDict)))
            t.start()
            myThreads.append(t)
        except:
            print ("Error: unable to start thread") 
    while(len(myThreads)):
        time.sleep(1)
        myThreads = [t for t in myThreads if t.is_alive()]
        print(int(timer()-start), "seconds", len(startingWords)-len(myThreads),"/",len(startingWords))
    print("__")
    print("Guesses")
    print("Len of words = "+str(len(words)))
    for key in testDict:
        print(key,"\n",testDict[key])
    end = timer()
    print("Took", end - start, "seconds")

    '''
    k=30
    startingWords = random.choices(words, k=k)

    #startingWords = ["scone","adieu","boink","penis","scare","notes","resin","tares","senor"]
    #startingWords=['abort','actor','adore','after','alert','alter','aorta','arose','atone','avert','cater','crate','earth','eater','extra','forte','grate','great','hater', 'heart', 'irate', 'later', 'metro', 'opera', 'other', 'otter', 'outer', 'ovate', 'overt', 'ratio', 'react', 'retro', 'roast', 'route', 'stare', 'store', 'taker', 'tamer', 'taper', 'tarot', 'teary', 'tenor', 'terra', 'tower', 'trace', 'trade', 'tread', 'treat', 'trope', 'trove', 'voter', 'water', 'wrote']

    for x,startingWord in enumerate(startingWords):
        print(str(x)+"/"+str(len(startingWords)))
        try:
            t = (threading.Thread(target=thread, args=(words, startingWords, letterDicts, attemptDict, x, startingWord, successDict, failureDict, guessingDict)))
            t.start()
            myThreads.append(t)
        except:
            print ("Error: unable to start thread") 

    print("__")
    print("Results")
    for res in sorted(attemptDict.items(), key=lambda item: item[1]):
        print(res)
    print("__")
    for key in guessingDict:
        print("Guesses",key)
        for guessHist in random.sample(guessingDict[key],10):
            print(guessHist)
    print("__")
    print("Success")
    for suc in sorted(successDict.items(), key=lambda item: item[1], reverse=True):
        print(suc)
    print("__")
    print("Failures")
    for fail in sorted(failureDict.items(), key=lambda item: item[1]):
        print(fail)
'''