# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 08:33:14 2016

@author: KimiZ


This script handles Lambda Functions.

*** lambda can take only a single expression ***
What is an expression?

- If it doesn’t return a value, it isn’t an expression and can’t be put into a lambda.

- If you can imagine it in an assignment statement, on the right-hand side of the equals sign, it is an expression and can be put into a lambda.
 
 https://pythonconquerstheuniverse.wordpress.com/2011/08/29/lambda_tutorial/
 
"""
from __future__ import division
import numpy as np
from numpy import log, sqrt

#########################################################
'''
##################       Using Lambda to filter lists and arrays.
'''

aList = [1,2,3,4,5,6,7,8,9]
low = 3
high = 7
filter(lambda x, l=low, h=high: h>x>l, aList)

def within_bounds(value, l=low, h=high):
    return h>value>l
filter(within_bounds, aList)

bList = np.arange(1,10,1); bList

def within_bounds(value, low=3, high=8):
    return high > value > low
filter(within_bounds, bList)


channels = np.arange(1,128,1)
def ch_cuts(value, lo=5, hi=125):
    return hi>value>low
new_channels = filter(ch_cuts, channels); new_channels

channels = np.arange(1,128,1)
filter(lambda value, lo=5, hi=125: hi>value>low, channels)
new_channels = filter(lambda value, lo=5, hi=125: hi>value>low, channels)

# removed all channels between 26 and 31.
good_channels = filter(lambda value, lo=25, hi=32: ((value<=lo) or (value>=hi)), new_channels)

new_channels.index(100) # returns 96


'''
##################       Using Lambda to set up functions.
'''


### THESE TWO RETURN THE SAME THING.  BOTH ARE FUNCTIONS
def square_root(x): return sqrt(x)
square_root(4)
type(square_root)

sq_rt = lambda x: sqrt(x)
sq_rt(4)
type(sq_rt)

summation = lambda x,y: x+y
summation(2,5)

ndata = 394; cstat = 311.12; k = 4

aic = lambda cstat, k: cstat - 2*k
aic(cstat, k)
aic(331.12,2)

bic = lambda cstat, k, ndata: cstat-k*log(ndata)
bic(cstat,k,ndata)


'''
##################       Conditionals with Lambda
'''
#lambda: a if some_condition() else b
check_int = lambda x: 1 if isinstance(x,int) else 0
check_int(3)
check_int(3.)
check_int('cool')

cList = [1,2,3,4,5]
check_existence = lambda x: 1 if x in cList else 0 
check_existence(3)
check_existence(9)


#lambda x: ‘big’ if x > 100 else ‘small’
guess = lambda x: 'yes' if x==24 else 'nope, try again'
guess(24)
guess(25)
guess(2)

guess = lambda x: 'yes' if 24 in x else 'nope, try again'
guess([1,2,3,24])
guess([1,2,3,4])
guess([1,2,3,4,99,2,4])
guess([24,25])


s1 = np.random.random_integers(-5, 5, 100) 
s2 = np.random.random_integers(-5, 5, 100) 
s3 = np.random.random_integers(-5, 5, 100)
s4 = np.random.random_integers(-5, 5, 100)  

s = []
for i in [s1,s2,s3,s4]:
    s.append(filter(lambda x: x!=0, i))
# s now contains all four lists s1, s2, s3 and s4 but without the 0's.


foo = np.arange(1, 100, 1)

# return everything that IS divisible by 2.
filter(lambda x: x % 2 == 0, foo)

# return anyting NOT devisible by 3.
filter(lambda x: x % 3, foo) 

# return anyting that IS devisible by 3.
filter(lambda x: x % 3 == 0, foo) 



'''
##################       MAPPING
'''
# map(function, iterable)
sentence = 'It is raining cats and dogs'
words = sentence.split()
print words
['It', 'is', 'raining', 'cats', 'and', 'dogs']

lengths = map(lambda word: len(word), words)
print lengths

name_list = ['kim','siri','derek']
person = 'kim'
map(lambda name: name is person, name_list)
map(lambda name: name is 'kim', name_list)
map(lambda name: 'k' in name, name_list)

### MAPPING WITH DICTIONARIES.
survey = {'Kim': ['biking', 'volleyball'], 'Derek': ['soccer', 'volleyball'], 'Stef': ['basketball', 'volleyball']}

map(lambda sport: 'volleyball' in sport, survey.values())
map(lambda sport: 'basketball' in sport, survey.values())

# we want to find out who all plays basketball.
plays_bball = filter(lambda sport: survey.keys() if 'basketball' in sport else 0, survey.values())
print(plays_bball, ' plays basketball')

kims_sports = survey.get('Kim') # returns ['biking', 'volleyball']
print("Kim plays: ", kims_sports)



'''
################## GUI programming with Lambda
'''
###  SEE THE FOLLOWING BLOG: 
# https://pythonconquerstheuniverse.wordpress.com/2011/08/29/lambda_tutorial/
import Tkinter as tk

def __init__(self, parent):
    """Constructor"""
    frame = tk.Frame(parent)
    frame.pack()
 
    btn22 = tk.Button(frame, 
        text="22", command=lambda: self.printNum(22))
    btn22.pack(side=tk.LEFT)
 
    btn44 = tk.Button(frame, 
        text="44", command=lambda: self.printNum(44))
    btn44.pack(side=tk.LEFT)





