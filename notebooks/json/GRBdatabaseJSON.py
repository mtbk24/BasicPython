# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:37:56 2017

@author: KimiZ
"""

from __future__ import division
import json
import os
#from collections import OrderedDict

def make_database(dbname, *args, **kwargs):
    '''
    dbname:  database name, 'database1.db' where dbname = 'database1'
    
    args:   a list of fieldnames.
    
    kwargs:  a dictionary of fields and content.
    '''
    models = ['grbm', 'sbpl', 'cutoffpl', 'grbm+bbody_v1', 'grbm+bbody_v2',  'sbpl+bbody_v1', 'sbpl+bbody_v2', 'cutoffpl+bbody_v1', 'cutoffpl+bbody_v2', 'grbm+lpow', 'sbpl+lpow', 'cutoffpl+lpow', 'grbm+bbody+lpow', 'sbpl+bbody+lpow', 'cutoffpl+bbody+lpow']
    
    if os.path.exists('%s.json'%(dbname)):
        raise Exception, "I will not overwrite an existing database."
    
    data = {}
    
    for mod in models:
    
        data.update({'%s'%mod: {'XSPECflags':    '', 
                           'XSPECnotes':    '', 
                           'BXAOflags':     '', 
                           'BXAOnotes':     '', 
                           'BXAAflags':     '', 
                           'BXAAnotes':     '', 
                           'BXAvsXSPEC':    '', 
                           'STATnotes':     '', 
                           'Notes':         ''
                           }
                           })
    json.dump(data, open('%s.json'%(dbname), 'w'), indent=4)
    
  

def make_updates(dbname, modelname, field, content, action='a'):
    '''
    modelname:  name of model you wish to update.
    
    field:     name of field to update.
    content:   content of the update.
    action:     'a' for append to what's already there.
                'w' for write over what is already there. 
                'w' will delete old content.
    
    ex:
    Notes = 'Xspec fit was poor.  Did not match data at high energies.'
    
    make_updates(dbname     = 'bn080916009_LAT',
                 modelname  = 'grbm', 
                 field      = 'XSPECnotes', 
                 content    = Notes,
                 action     = 'a')
    

    
    '''
    
    
    with open("%s.json"%(dbname), "r") as jsonFile:
        data = json.load(jsonFile)

    if 'a' in action:
        tmp = data['%s'%(modelname)]['%s'%(field)]
        data['%s'%(modelname)]['%s'%(field)] = tmp + ' ' + content
    elif 'w' in action:
        answer = raw_input('Are you sure you want to write over old content? \
        y or n   \n')
        if 'y' in answer:
            data['%s'%(modelname)]['%s'%(field)] = content
        else:
            'Not overwriting file contents.'
            pass

    with open("%s.json"%(dbname), "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)
        
    
def read_database(dbname, model=None, field=None):
    f  = open("%s.json"%(dbname), 'r')
    db = json.load(f)
    f.close()

    if (model is not None) and (field is not None):
        print('\n ***   %s   %s   *** '%(model, field))
        print('%s:  %s \n'%(field, db['%s'%(model)]['%s'%(field)]))  
        #print( db['%s'%(model)]['%s'%(field)] )
    elif (model is not None) and (field is None):
        print('\n ***   %s   ***'%(model))
        z = db['%s'%(model)]
        for i,j in enumerate(z):
            print("%s:  %s \n"%(j, z[j]))
    else:
        print( db ) 
    return db
        



name = 'bn110731465_LAT'
#   make_database(name)  


model   = 'sbpl+bbody+lpow'
field   = 'BXAAnotes'
NOTES   = 

model               = 'sbpl+bbody+lpow'
XSPECflags          = ''
XSPECnotes          = ''

BXAOflags           = ''
BXAOnotes           = ''

BXAAflags           = ''
BXAAnotes           = 'PL insignificant and marginals have large variance in this component.'
BXAvsXSPEC          = ''
STATnotes           = ''
Notes               = ''  


#NOTES = 'kim rocks the socks off of this one!'
NOTES = 'done with this shit'
make_updates(name, 'grbm', 'XSPECnotes', NOTES, 'w')    
    
    
    
kim = read_database(name, 'grbm', 'XSPECnotes')   

read_database(name, 'grbm', 'XSPECnotes');

read_database(name, 'grbm');




    
    
#    
#model               = 'sbpl+bbody+lpow'
#XSPECflags          = ''
#XSPECnotes          = ''
#
#BXAOflags           = ''
#BXAOnotes           = ''
#
#BXAAflags           = ''
#BXAAnotes           = 'PL insignificant and marginals have large variance in this component.'
#BXAvsXSPEC          = ''
#STATnotes           = ''
#Notes               = ''    
#
#
#
#make_updates(name, model, 'BXAAnotes', BXAAnotes)  

