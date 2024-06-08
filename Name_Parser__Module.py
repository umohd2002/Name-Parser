# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 20:27:31 2023

@author: Salman Khan
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json
from ORM import MaskTable, ComponentTable, MappingJSON, User, UserRole, ExceptionTable, MapCreationTable
# from LoginORM import UserRole, User
import re
import io
from tqdm import tqdm
import Rulebased as RuleBased
import pandas as pd
import json 
import collections 
import PreprocessingName as PreProc
import sklearn
from sklearn.metrics import multilabel_confusion_matrix,confusion_matrix,classification_report
from flask import session

#Parsing 1st program
from DB_Operations import DB_Operations
import zipfile
import os
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
today=datetime.today()
current_time = datetime.now().time()

# Format the time as HH:MM:SS
time_string = current_time.strftime("%H:%M:%S")

def Name_Parser(Name_4CAF50,Progress,TruthSet=""):
    Result={}
    RuleBasedOutput={}
    Exception_Mask=""
    FishBone=""
    Detailed_Report=""
    Mask_log={}
    Unique_Mask={}
    db_operations = DB_Operations(database_url='sqlite:///KnowledgeBase.db')
    Name_4CAF50=open(Name_4CAF50,"r",encoding='utf8')
    file_name = os.path.splitext(os.path.basename(Name_4CAF50.name))[0]
    Lines = Name_4CAF50.readlines()
    
    # file_name = os.path.splitext(os.path.basename(Name_4CAF50.filename))[0]
    # Lines = Name_4CAF50.readlines()
    
    
    
    # Lines = [line.decode('utf-8') if isinstance(line, bytes) else line for line in Lines]

    fileHandle = open('NamesWordTable.txt', 'r',encoding="utf8")



    # Strips the newline character
    Observation=0
    Total=0
    Truth_Result={}
    dataFinal={} 
    USAD_Conversion_Dict={
      "PRE_TLE": 1,
      "SUR_NME": 2,
      "GIV_NME": 3,
      "GEN_SFX": 4,
      "SUF_TLE": 5
    }
    data={}
    data = db_operations.get_data_for_all()

    # print("KwoledgeBase Data: ", data)
    component_dict = {}
    component_dict = db_operations.get_components()
    # print("\n Component Dict: ", component_dict)

    # with open('JSONMappingDefault.json', 'r+', encoding='utf8') as f:
    #     data = json.load(f)
    USAD_CONVERSION_={

       "PRE_TLE": 1,
       "SUR_NME": 2,
       "GIV_NME": 3,
       "GEN_SFX": 4,
       "SUF_TLE": 5
    }
    Detailed_Report+="Exception and Mask Report\n"
    ExceptionList = []
    WordTable={}

# =============================================================================
#     for line in fileHandle:
#      
#         fields=line.split('|')
#         print("field",fields)
# =============================================================================
        #WordTable[fields[0].strip()]=fields[1][0].strip()
        #print(WordTable[fields[0]])
    # Progress.start()
    CNT=100/len(Lines)
    CN=0
    for line in tqdm(Lines, desc="Processing"):
        CN=CN+CNT
        # Progress["value"]=CN
        line=line.strip("\n").split("|")
        ID=line[0].strip()
        try:
            
            line=line[1].strip()
        except:
            continue
        Name=line
        FirstPhaseList=[]
        PackName=PreProc.PreProcessingName().NamesCleaning(line)
        NameList=PackName[0]
        NameList = [i for i in NameList if i]
      
        TrackKey=[]
        Mask=[]
        Combine=""
        LoopCheck=1
        for A in NameList:
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
                        break  
                    elif SP.strip() == clue[0] and clue[1].strip() == 'L':
                        found_l = True
                        break  
                
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
                    if A== fields[0].strip() :
                        NResult=True
                        temp=fields[1].strip()
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
            
        Mask_1=",".join(Mask)
        
        print(Mask_1, "SDASD")
        Mask_log[ID]=Mask_1
        print(Mask_1, "SDASD")
        Unique_Mask[Mask_1]=ID
        print(Mask_1, "SDASD")
        FirstPhaseList = [FirstPhaseList[b] for b in range(len(FirstPhaseList)) if FirstPhaseList[b] != ","]
        # print("FirstPhaseList: ",FirstPhaseList)
        Found=False
        FoundDict={}
        print(FirstPhaseList)
        print(db_operations.check_mask_exists("PWIWG"))
        if db_operations.check_mask_exists(Mask_1):
            print(Mask_1)
            FoundDict[Mask_1]= db_operations.get_data_for_mask(Mask_1)
            Found=True
            
        
        # if db_operations.check_mask_exists(Mask_1):
        #     # Mask exists in the database, retrieve data using database queries
        #     FoundDict[Mask_1] = db_operations.get_data_for_mask(Mask_1)
        #     # print("FoundDict: ",FoundDict[Mask_1])
        #     Found = True
            # print("Found Dict = ",FoundDict[Mask_1])
        sorted_Found = {}
        if Found:
            Observation+=1
            Mappings=[]
            for K2,V2 in FoundDict[Mask_1].items():
                FoundDict_KB=FoundDict[Mask_1]
                sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
            # print("sorted_Found: ",sorted_Found)
            for K2,V2 in sorted_Found.items():
                Temp=""
                Merge_token=""
                for p in V2:
                    for K3,V3 in FirstPhaseList[p-1].items():
                       Temp+=" "+V3
                       Temp=Temp.strip()
                       Merge_token+=K3
                       found = False
                       for entry in Mappings:
                           if entry[0] == K2:
                               # Append V3 to existing entry
                               entry[1] += K3
                               entry[2] = ""
                               entry[2] += Temp
                               found = True
                               break
                       if not found:
                         # Add a new entry to Mappings
                           Mappings.append([K2, K3, V3])

            FoundDict_KB=FoundDict[Mask_1]
            sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
            
            
            OutputEntry = {
                "Record ID": ID,
                "INPUT": Name,
                str(Mask_1): Mappings
            }
            OutputList = []
            OutputList.append(OutputEntry)
            # print(OutputList)
            try:
                Truth_Result[ID]=Mappings
                Result[ID]=OutputList
                dataFinal[Mask_1][ID] =Mappings # <--- add `id` value.
                
            except: 
                Result[ID]=OutputList
                Truth_Result[ID]=Mappings
                dataFinal[Mask_1]={}
                dataFinal[Mask_1][ID]=Mappings
                
                
            
        else :
            NameList=[item for item in NameList if item!=","]
            rules=RuleBased.RuleBasedNameParser.NameParser(NameList)
            for m in rules:
                component = m[1]
                if component not in component_dict.keys():
                    component_description = "Not Selected"
                    m[1] = "USAD_NA"
                    m.append(component_description)
                else:
                    component_description = component_dict[component]
                    m.append(component_description)

                # print(f"{component} : {component_description}")
            ExceptionEntry = {
                "Record ID": ID,
                "INPUT": Name,
                str(Mask_1): rules
            }
            ExceptionList.append(ExceptionEntry)
            RuleBasedOutput[ID]=rules
        # else:
        #     try:
                    
        #         RuleBasedOutput[ID]=RuleBased.RuleBasedNameParser.NameParser(NameList)
        #         Exception_Mask+=Mask_1+"\n"
        #     except:
        #         continue
        Total+=1
   
    Count_of_Correct=0
    Total_Count=0  
    y_test=[]
    y_predict=[]
    # with open("Individual Name1_Truth_File.txt", 'r+', encoding='utf-8') as g:

    #     Stat = json.load(g)
    #     Count_of_Correct=0
    #     Total_Count=0
                
    #     for key,value in Truth_Result.items():
    #         Total_Count=len(Truth_Result)

    #         if key in Stat.keys():
    #             Count1=0
    #             Count_total=0
    #             for k1,v1 in value.items():
    #                 predict=False
    #                 y_test.append(USAD_Conversion_Dict[k1])
    #                 for k2,v2 in Stat[key].items():
    #                     if v1==v2:
    #                         y_predict.append(USAD_Conversion_Dict[k2])
    #                         Count1+=len(Stat[key])
    #                         predict=True
    #                         break
    
    #                 if not predict:
    #                     for f in v1.split(" "):
    #                         for k2,v2 in Stat[key].items():
    #                             if f in v2:
    #                                 y_predict.append(USAD_Conversion_Dict[k2])
    #                                 predict=True
    #                                 break
    #                         if predict:
    #                             break
    #                         else:
    #                             y_predict.append(0)
    
    
    # Exception_file_name = "_MultiLine_ExceptionFile" + str(current_time) + ".json"
    # Exception_file_name = file_name +" "+ str(current_time) + ".json"
    # Exception_file_name = re.sub(r'[^\w_. -]', '_', Exception_file_name)
    # path = 'Exceptions/MultiLine Exceptions/' + Exception_file_name
    # exception_File = "Output/Downloads/Exception"+ file_name + "_Exception.json"
    # with open(exception_File, 'w', encoding='utf-8') as g:
    #     g.seek(0)
    #     json.dump(ExceptionList, g, indent=4)
    #     g.truncate
    
    FishBone+="Root Cause Analysis"
    if TruthSet!="":
        try:
            with open(TruthSet, 'r+', encoding='utf-8') as g:
                Stat = json.load(g)
                Count_of_Correct=0
                Total_Count=0
                ID=1
                False_Predictions={}
                
                        
                for k in Stat["annotations"]:
                    res=""
                    False_Predictions_Indiv={}
                    
                    for m in k[1].items():
                        
                        for j in m[1]:
                            predict=False
                            y_test.append(USAD_Conversion_Dict[j[2]])
                            Found_Error=False
                            for k1,v1 in Truth_Result[str(ID)].items():
                                if re.sub('\W+','', v1.strip().upper()) == re.sub('\W+','', k[0][j[0]:j[1]].upper().strip()):
                                    
                                    if k1!=j[2]:
                                        Found_Error=True
                                        False_Predictions_Indiv_1={}
                                        False_Predictions_Indiv_1["Correct Class"]=j[2]
                                        False_Predictions_Indiv_1["Incorrect Class"]=k1
                                        False_Predictions_Indiv_1["Value"]=v1
                                        False_Predictions_Indiv["Mask"]=Mask_log[str(ID)]
                                        False_Predictions_Indiv["Raw Name"]=k[0]
                                        False_Predictions_Indiv[str(k1)+"_"+str(j[2])]=False_Predictions_Indiv_1
                                    y_predict.append(USAD_Conversion_Dict[k1])
                                    
                                    predict=True
                                    break
                            if Found_Error:    
                                False_Predictions[ID]=False_Predictions_Indiv
                            
                            if not predict:
                                #y_predict.append(0)
                                y_test.pop()         
                    ID+=1
        except:
            return (False,"Error in the selected file! try again")
        import numpy as np
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        Confusion =  multilabel_confusion_matrix(y_test, y_predict)
        df=classification_report(y_test,y_predict,output_dict=True)
        df_report = pd.DataFrame(df).transpose()
        df_report.reset_index(inplace=True)
        df_report=df_report.replace({"index": USAD_CONVERSION_})
        df_report.to_csv("Metrics.csv")
        
        RTruth=0
        try:
            RTruth=(Count_of_Correct/Total_Count*100)
        except:
            print()
        Detailed_Report+="Output From Active Learning\n\n"
        ActiveLResult = json.dumps(Result, indent = 4,ensure_ascii=False) 
        Detailed_Report+=str(ActiveLResult)
        
        RootCauseReport= json.dumps(False_Predictions, indent=4, ensure_ascii=False)
        
        FishBone+="\n\n"+str(RootCauseReport)
        RuleBasedRes =json.dumps(RuleBasedOutput,indent=4)
        Detailed_Report+="\n\nOutput Fron Rule Based Approach\n\n"
        Detailed_Report+=str(RuleBasedRes)
        Detailed_Report+="\n\nNumber of Exceptions Thrown: -\t"+str(Total-Observation)+"\n"
        Detailed_Report+="Number of Parsed Name: -\t"+str(Observation)+"\n"
        Detailed_Report+="Percentage of Parsed Result: -\t"+str((Observation/Total)*100)+"\n"
        Detailed_Report+="List of Exception Mask(s): -\t\n\n"+Exception_Mask+"--"
        Detailed_Report+="\n\n Evaluation Metrics\n\n"
    
        Detailed_Report+=str(df_report)
        f=open(f"Detailed_Report {file_name}.txt","w",encoding="utf8")
        f1=open(f"Root Cause Report {file_name}.txt","w",encoding="utf8")
        f1.write(FishBone)
        f1.close()
        f.write(Detailed_Report)
        f.close()
        return (True,f"Detailed_Report of {file_name} and Root Cause Report of {file_name} is Generated!")
    else:
        percentage = (Observation/Total)*100
        percentage = "%.2f"% percentage
        # ActiveLResult = json.dumps(Result, indent = 4,ensure_ascii=False) 
        # Detailed_Report+="\nNumber of Exceptions Thrown: -\t\t"+"{:,}".format(Total-Observation)+"\n"
        Detailed_Report="\nTotal Number of Names: -\t"+"{:,}".format(Total)+""
        Detailed_Report+="\nUnique Pattern Count: -\t"+"{:,}".format(len(Unique_Mask))+"\n\n"
        Detailed_Report+="\nNumber of Pattern Parsed Names: -\t"+"{:,}".format(Observation)+"\n"
        Detailed_Report+="Percentage of Patterns Parsed Result:  -\t"+"{:.2f}%".format(float(percentage))+"\n"
        Detailed_Report+="\nNumber of Exceptions Thrown: -\t\t"+"{:,}".format(Total-Observation)+"\n"
        Detailed_Report+="Percentage of RuleBased Parsed Result: -\t"+"{:.2f}%".format(100-float(percentage))+"\n"
        # Detailed_Report+="Output From Active Learning\n\n"
        # Detailed_Report+=str(ActiveLResult)
        
        # RuleBasedRes =json.dumps(RuleBasedOutput,indent=4)
        # Detailed_Report+="\n\nOutput Fron Rule Based Approach\n\n"
        # Detailed_Report+=str(RuleBasedRes)
        # detailed_report_file = "Output/Downloads/detailed_report.txt"
        # active_learning_file = "Output/Downloads/active_learning_output.json"
        # rulebased_output_file = "Output/Downloads/rulebased_output.json"
        # zip_file_name = f"Output/Batch File Output/{file_name}_output.zip"
        # # zip_file_name = re.sub(r'[^\w_. -]', '_', zip_file_name)
        
        # with open(detailed_report_file, "w", encoding = "utf8") as file:
        #     file.write(Detailed_Report)

        # # Writing the active learning output to a JSON file
        # with open(active_learning_file, "w", encoding = "utf8") as file:
        #     file.seek(0)
        #     json.dump(Result, file, indent=4)
        #     file.truncate

        # # Writing the rule-based output to a JSON file
        # with open(rulebased_output_file, "w", encoding = "utf8") as file:
        #     file.seek(0)
        #     json.dump(RuleBasedOutput, file, indent=4)
        #     file.truncate
        
        # with open(exception_File, "w", encoding = "utf8") as file:
        #     file.seek(0)
        #     json.dump(ExceptionList,file,indent=4)
        #     file.truncate
        
        # with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        #     zipf.write(detailed_report_file)
        #     zipf.write(active_learning_file)
        #     zipf.write(rulebased_output_file)
        #     zipf.write(exception_File)


        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # Create in-memory byte streams for your files
        detailed_report_stream = io.BytesIO()
        active_learning_stream = io.BytesIO()
        rule_based_output_stream = io.BytesIO()
        # exception_stream = io.BytesIO()

        # Write the contents to the byte streams
        detailed_report_stream.write(Detailed_Report.encode('utf-8'))
        active_learning_stream.write(json.dumps(Result, ensure_ascii=False, indent=4).encode('utf-8'))
        rule_based_output_stream.write(json.dumps(RuleBasedOutput, indent=4,ensure_ascii=False).encode('utf-8'))
        # exception_stream.write(json.dumps(ExceptionList, indent=4, ensure_ascii=False).encode('utf-8'))
        # print("File banri ruko!")
        # Make sure to seek to the start of each stream after writing
        detailed_report_stream.seek(0)
        active_learning_stream.seek(0)
        rule_based_output_stream.seek(0)
        # exception_stream.seek(0)

        # File names
        detailed_report_file_name = f"Detailed Report_{file_name}.txt"
        active_learning_file_name = f"Active Learning Output.json"
        rule_based_output_file_name = f"Rule Based Output.json"
        # exception_file_name = f"{file_name}_Exception File_{str(current_time)}.json"
        zip_file_name = f"Output/Batch File Output/{file_name}_output.zip"
        try:
        # Create a zip file and write the byte streams to it
            with zipfile.ZipFile(zip_file_name, 'w') as zipf:
                zipf.writestr(detailed_report_file_name, detailed_report_stream.getvalue())
                zipf.writestr(active_learning_file_name, active_learning_stream.getvalue())
                zipf.writestr(rule_based_output_file_name, rule_based_output_stream.getvalue())
                # zipf.writestr(exception_file_name, exception_stream.getvalue())
        except Exception as e:
            print(f"Error creating zip file: {e}")

        # No need to return a message about generating files since they aren't generated on the filesystem
        # return (True, f"Zip file '{zip_file_name}' has been created with all reports.")


            
        # Detailed_Report+="List of Exception Mask(s): -\t\n\n"+Exception_Mask+"--"
        # Detailed_Report_1="\nTotal Number of Names: -\t\t\t"+"{:,}".format(Total)+""
        # Detailed_Report_1+="\nUnique Pattern Count: -\t\t\t\t"+"{:,}".format(len(Unique_Mask))+"\n"
        # Detailed_Report_1+="\nNumber of Pattern Parsed Names: -\t"+"{:,}".format(Observation)+"\n"
        # Detailed_Report_1+="Percentage of Patterns Parsed Result:  -\t"+"{:.2f}%".format(float(percentage))+"\n"
        # Detailed_Report_1+="\nNumber of Exceptions Thrown: -\t\t\t"+"{:,}".format(Total-Observation)+"\n"
        # Detailed_Report_1+="Percentage of RuleBased Parsed Result: -\t"+"{:.2f}%".format(100-float(percentage))+"\n"
        # Detailed_Report_1+="List of Exception Mask(s): -\t\n\n"+Exception_Mask+"--"
        # Output_file_name = "Detailed_Report_" + str(current_time) + ".txt"
        # Output_file_name = "Detailed Report_"+file_name+".txt"
        # Output_file_name = re.sub(r'[^\w_. -]', '_', Output_file_name)
        # path = 'Output/Batch File Output/' + Output_file_name
        abs_path = os.path.abspath(zip_file_name)
        # f=open(path,"w",encoding="utf8")
        # f.write(Detailed_Report)
        # f.close()
        
        #---------------------------------------------------------------------------------
        #Just Evaluations
        
        # print(Mask_1)
        # print("\n Other Without ID: ",Mask_log)
        # print(FirstPhaseList)
        
        #---------------------------------------------------------------------------------
        
        # Progress.stop()

        # print(zip_file_name)
        # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
        Session = sessionmaker(create_engine('sqlite:///KnowledgeBase.db'))
        sessions = Session()
        mapdata_list = []
        exc_data_list = []
        for i in ExceptionList:
            rules = i
            excdata = {
                "Timestamp": timestamp,
                "Username": session["user_id"],
                "Run": "Multiple",
                "Record ID": rules["Record ID"],
                "data": rules[next((key for key, value in rules.items() if isinstance(value, list)), None)]
            }
            mapdata = MapCreationTable(Name_Input=rules["INPUT"], Mask=next((key for key, value in rules.items() if isinstance(value, list)), None))
            mapdata_list.append(mapdata)
            # Wait until the mapdata object is added to get the ID
            sessions.add(mapdata)
            sessions.flush()  # Required to generate the ID for mapdata before using it
            j = 1
            for data in excdata["data"]:
                exc_data = ExceptionTable(
                    UserName=excdata["Username"], 
                    Timestamp=excdata["Timestamp"], 
                    Run=excdata["Run"], 
                    Name_ID=excdata["Record ID"], 
                    Component=data[1], 
                    Token=data[0], 
                    Mask_Token=data[2], 
                    Component_index=j, 
                    MapCreation_Index=mapdata.ID
                )
                exc_data_list.append(exc_data)
                j += 1
        # Add all the records in a batch
        sessions.add_all(mapdata_list + exc_data_list)
        # Commit the transaction
        sessions.commit()
        return (True,f"Detailed_Report of {file_name}.txt is Generated! \n\nThe {file_name}_Output.zip is downloaded, please check your download's directory. \n\n{Detailed_Report}", zip_file_name)

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
# Name_Parser("SampleName.txt")

