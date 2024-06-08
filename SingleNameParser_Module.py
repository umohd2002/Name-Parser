# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 21:33:57 2023

@author: Salman Khan
"""


import re
# from tqdm import tqdm
# import pandas as pd
import json 
# import collections 
#Parsing 1st program
# import re
import os.path
import collections                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
import Rulebased as rulebased
import PreprocessingName as PreProc
from DB_Operations import DB_Operations

from datetime import datetime,timedelta
today=datetime.today()
current_time = datetime.now().time()
time_string = current_time.strftime("%H:%M:%S")
unique = timedelta(microseconds=-1)



file_dir = os.path.dirname(os.path.realpath('__file__'))


from pathlib import Path

root_folder = Path(__file__).parents[1]

ExceptionList = []
def throwException(originalInput,initials):
    db_operations = DB_Operations(database_url='sqlite:///KnowledgeBase.db')
    PackName=PreProc.PreProcessingName().NamesCleaning(originalInput)
    component_dict = {}
    component_dict = db_operations.get_components()
    # print("\n Component Dict: ", component_dict)
    # NameList = re.split("\s|\s,\s ", Name)
    NameList = PackName[0]
    NameList= [item for item in NameList if item]# != ","]
    rules=rulebased.RuleBasedNameParser.NameParser(NameList)
    # print("Rules: ",rules)
    for m in rules:
        component = m[1]
        if component not in component_dict.keys():
            m[1] = "NA"
            m.append("Not Selected")
        else:
            m.append(component_dict[component])
    # print("M: ",m)
    
    ID = "1"
    ExceptionDict = {
        "Record ID": ID,
        "INPUT": originalInput,
        str(Mask_1): rules
    }
    # oldExceptionList = ExceptionList.append(ExceptionDict)
    
    if ExceptionList:
        ExceptionList[0]= ExceptionDict
        
    else:
        ExceptionList.append(ExceptionDict)
    
    
    
    # Exception_file_name = initials+" " +str(current_time) +"_Forced_ExceptionFile.json"
    # Exception_file_name = re.sub(r'[^\w_. -]', '_', Exception_file_name)
    # path = 'Exceptions/ForcedExceptions/' + Exception_file_name
    # with open(path, 'w', encoding='utf-8') as g:
    #     g.seek(0)
    #     json.dump(ExceptionList, g, indent=4)
    #     g.truncate
        

    return True, ExceptionList


def Name_Parser(line,initials,originalInput):
    global Result, Exception_file_name, FirstPhaseList, Mask_1, NameList, rules
    Result={}
    db_operations = DB_Operations(database_url='sqlite:///KnowledgeBase.db')
    Exception_=False
    Exception_file_name=""
    fileHandle = open('NamesWordTable.txt', 'r',encoding="utf8")
    # Strips the newline character
    Observation=0
    Total=0
    Truth_Result={}
    dataFinal={}
    # Name = line
    FirstPhaseList=[]
    PackName=PreProc.PreProcessingName().NamesCleaning(line)
    # NameList = re.split("\s|\s,\s ", Name)
    NameList = PackName[0]
    NameList= [item for item in NameList if item]# != ","]
    #del(NameList[len(NameList)-1])
    TrackKey=[]
    Mask=[]
    Combine=""
    LoopCheck=1
    ID = "1"
    component_dict = {}
    component_dict = db_operations.get_components()
    print("\n Component Dict: ", component_dict)
    for A in NameList:
        A= A.strip()
        FirstPhaseDict={}
        NResult=False
        if A==",":
            O=0
            Mask.append(Combine)
            Combine=""
            FirstPhaseList.append(",")
            #FirstPhaseList.append("Seperator")
        elif A==" ":
            continue
        elif A!="," and len(A)==1:
            
            NResult=True
            Combine+="I"
            TrackKey.append("I")
            FirstPhaseDict["I"] = A
            FirstPhaseList.append(FirstPhaseDict)
        elif '-' in A:
            FP, SP = A.split('-')
            found_l = False  # Flag to track if either FP or SP matches the condition
            for clues in fileHandle:
                clue = clues.split('|')
                if FP == clue[0] and clue[1].strip() == 'L':
                    found_l = True
                    break  # Exit the loop if FP matches the condition
                elif SP.strip() == clue[0] and clue[1].strip() == 'L':
                    found_l = True
                    break  # Exit the loop if SP matches the condition
            
            if found_l:
                Combine += "L"
                TrackKey.append("L")
                FirstPhaseDict["L"] = A
                FirstPhaseList.append(FirstPhaseDict)
            else:
                Combine += "W"
                TrackKey.append("W")
                FirstPhaseDict["W"] = A
                FirstPhaseList.append(FirstPhaseDict)
        else:
            for line in fileHandle:
                fields=line.split('|')
                if A==(fields[0]):
                    NResult=True
                    temp=fields[1]
                    Combine+=temp[0]
                    FirstPhaseDict[temp[0]] = A
                    FirstPhaseList.append(FirstPhaseDict)
                    TrackKey.append(temp[0])
            if NResult==False:
                Combine+="W"
                TrackKey.append("W")
                FirstPhaseDict["W"] = A
                FirstPhaseList.append(FirstPhaseDict)
        if LoopCheck==len(NameList):
            Mask.append(Combine)
        fileHandle.seek(0)
        LoopCheck+=1
    print(Mask)
    Mask_1=",".join(Mask)
    FirstPhaseList = [FirstPhaseList[b] for b in range(len(FirstPhaseList)) if FirstPhaseList[b] != ","]
    # data={}
    # with open('JSONMappingDefault.json', 'r+', encoding='utf-8') as f:
    #     data = json.load(f)
    Found=False
    FoundDict={}
    # for tk,tv in data.items():
    #     if(tk==Mask_1):
    #         FoundDict[tk]=tv
    #         Found=True
    #         break

    
    if db_operations.check_mask_exists(Mask_1):
        print(True)
        FoundDict[Mask_1] = db_operations.get_data_for_mask(Mask_1)
        Found = True
    
    
    
    if Found:
        Observation+=1
        Mappings=[]
        uiMappings = []
        for K2,V2 in FoundDict[Mask_1].items():
            FoundDict_KB=FoundDict[Mask_1]
            sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
        dict_found={}
        for k,v in sorted_Found.items():
            for i in v:
                print('k',k,'k')
                dict_found[i]=k
                
        nest_list=[]
        # print(dict_found)
        mask=Mask_1.replace(",","")
        for i in range(0,len(FirstPhaseList)):
            token=""
            for k,v in FirstPhaseList[i].items():
                token=v
                print(component_dict[dict_found[i+1]])
                component_description = component_dict[dict_found[i+1]]
            uiMappings.append([token,dict_found[i+1],mask[i],component_description])
        # print("UiMappings: ",uiMappings)
        
        for K2,V2 in sorted_Found.items():
            Temp=""
            Merge_token=""
            for p in V2:
                for K3,V3 in FirstPhaseList[p-1].items():
                   Temp+=" "+V3
                   Temp=Temp.strip()      
                   Merge_token+= ""+K3
                   found = False
                   for entry in Mappings:
                       if entry[0] == K2:
                           
                           entry[1] += K3
                           entry[2] = ""
                           entry[2] += Temp
                           found = True
                           break
                   if not found:
                       Mappings.append([K2, K3, V3])
                       break

        FoundDict_KB=FoundDict[Mask_1]
        sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
                  
        try:
            Result["Input"]= originalInput
            Result["Output"]=uiMappings
            # messagebox.showinfo("Success!",f"{originalInput}\n\nName Successfully Parsed!\n\nOutput derived from Active Learning")
        except:
            Result["Input"]= originalInput
            Result["Output"]=uiMappings
            # messagebox.showinfo("Success!",f"{originalInput}\n\nName Successfully Parsed!\n\nOutput derived from Active Learning")

        
        
        OutputDict = {
                "Record ID": ID,
                "INPUT": originalInput,
                str(Mask_1): Mappings
            }
        # Output_file_name=initials+str(current_time)+"_Output.json"
        # Output_file_name=re.sub(r'[^\w_. -]', '_', Output_file_name)
        # path= 'Output/Single Line Output/'+Output_file_name
        # with open(path,'w', encoding='utf-8') as g:
        #     g.seek(0)
        #     # Stat=originalInput,Mappings
        #     json.dump(OutputDict,g,indent=4)
        #     g.truncate
        
    else:
        Exception_=True
        rules=rulebased.RuleBasedNameParser.NameParser(NameList)
        # print(rules)
        ExceptionDict = {
            "Record ID": ID,
            "INPUT": originalInput,
            str(Mask_1): rules
        }
        Result["Input"]=originalInput
        Result["Output"]=rules
        for m in Result["Output"]:
            component = m[1]
            # print("Component: ",component)
            # component_description = db_operations.get_component_description(component)
            # print("description : ",component_description)
            if component not in component_dict.keys():
                m[1] = "NA"
                m.append("Not Selected")
            else:
                m.append(component_dict[component])
        # print(Result["Output"])
        # messagebox.showwarning("Exception!",f"Exception is Created for the Name\n\n{originalInput}\n\nOutput Derived from Rulebased Learning")

        
        if ExceptionList:
            ExceptionList[0] = ExceptionDict
            
        else:
            ExceptionList.append(ExceptionDict)
        # Exception_file_name = initials+ " " + str(current_time) + "_ExceptionFile.json"
        # Exception_file_name = re.sub(r'[^\w_. -]', '_', Exception_file_name)
        # path = 'Exceptions/SingleException/' + Exception_file_name
        # with open(path, 'w', encoding='utf-8') as g:
        #     json.dump(ExceptionList, g, indent=4)
        #     g.truncate
            
        
       
        
        
    Total+=1
   
    return (Result, Mask_1,Exception_file_name, throwException,Exception_)

# Convert=Name_Parser("5506 A Street 324 2535 64356 3452323 Little, Rock, AR 72205",'initial',"5506 A Street Little Rock AR 72205")
# Result=Convert[0]
# print(Result)
# print(type(Result))

# print("Final Correct Name Parsing Percentage",Count_of_Correct/Total_Count*100)
# print("Name Matching Report")
# print("Total=",Count)
# print("Matched Names=",Observation)
# print("Percentage of Matched",(Observation/Count)*100)
        # print("Mask Generated is ",Mask_1)
    # print("Index\tMaskToken\t\tName Token")
    # i=1
    # for k in FirstPhaseList:
    #     for key,value in k.items():
    #         print(i,"\t\t",key,"\t\t\t\t",value) 
    #     i+=1