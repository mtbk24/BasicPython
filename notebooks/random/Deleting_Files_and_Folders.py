# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:38:53 2017

@author: KimiZ
"""

import os, glob

basedir = "/Users/KimiZ/GRBs2/analysis/pyxspec_programs/Analysis/"


burst       = "bn131231198"

detdir      = "GBM"     # GBM or GBMwLAT

methoddir   = "PYXSPEC"     #'PYXSPEC' or 'BXA'




model1      = "blackb"
model2      = "copl"

direc = "/Users/KimiZ/GRBs2/analysis/LAT/%s/%s/"%(burst, methoddir)

os.chdir(direc)

direcs1 = glob.glob("%s/*%s*"%(detdir, model1))
direcs2 = glob.glob("%s/*%s*"%(detdir, model2))

direcs0 = direcs1+direcs2
direcs0 = list(set(direcs0))


print("\n")
print(direcs0)
print("\n")

os.system("open %s"%(direc + detdir))


#%%

for i,j in enumerate(direcs0):
    if ('cutoffpl' in j) or ('bbody' in j):
        raise Exception, "Will not delete j"
    os.chdir(direc + j)
    print("\n"*2)
    print("---"*15)
    print("---"*15)
    print("        FILES:   ")
    !ls
    print("---"*15)
    print("\n Are you sure you want to delete all files in: ")
    # curdir is direc you will end up deleting
    curdir = os.getcwd()
    print("    %s"%curdir)
    answer = raw_input("y to delete all files:   ")
    if answer == "y":
        print("  Deleting now...   ")
        !rm *
        if os.path.exists('.DS_Store'):
            !rm .DS_Store
        os.chdir(direc)
        os.rmdir(curdir)
    else:
        print("  Moving on ...   ")
        os.chdir(direc)

print("\n"*3)   
print("*****************  DONE  *****************")   
%reset