# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:50:21 2023

 

@author: onais
"""

import re

 

 

class PreProcessingName:
    def __init__(self):
        self
    def NamesCleaning(self,line):
        line=line.lstrip(',')
        line=re.sub(r'[^a-zñáéíóúüÑÁÉÍÓÚÜA-Z0-9\s#,-]+', '',line)

        Name=re.sub(' +', ' ',line)
        Name=re.sub(',',' , ',Name)
        # Name=re.sub('#',' # ',Name)
        
        Name=Name.upper()

        NameList = re.split("\s|\s,\s", Name)
        try:
            NameList.remove("")
        except:
            True


        return (NameList,Name)
    
# cleaning = PreProcessingName.NamesCleaning(0,"1701 westpark drive, apt #&%105, Little Rock, AR 72204")
# print(cleaning)