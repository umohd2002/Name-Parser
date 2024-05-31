# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 01:23:26 2023

@author: Onais, Salman, Kashif
"""

import tkinter as tk
from tkinter import messagebox
from datetime import date
from tkinter import ttk

import tkinter as tk					
from tkinter import ttk,simpledialog,DISABLED
from datetime import date
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import pandas as pd
from functools import partial
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM import MaskTable, MappingJSON
import NameParser___Module as NModule
import NameAddressParser__Module as NaM
import Address_Parser__Module as AdM
import SingleNameParser_Module as NAD_API
import SingleAddressParser_Module as AD_API
import SingleNameAddressParser_Module as ADN_API
from datetime import datetime
import os
import subprocess
import hashlib
import Address_parser_mixc_methods as mx
import submission_form_parser as submissionform
import Address_parser_approval_form as approvalform


class submission_form:
    def clear_form(self,form_frame,canvas,table_frame,df,scrollbar,RevisedJSON):
    #------------------------------------------------------
        components = form_frame.winfo_children()
        scrollbar.destroy()
        for component in components:
            component.destroy()
        
        components=table_frame.winfo_children()
        
        for componenet in components:
            component.destroy()
        
        components = canvas.find_all()
        # Remove each component from the canvas
        for component in components:
            canvas.delete(component)
  
        RevisedJSON.pop(0)
        
        #---------------------------------------------------
    def submit_form(self,Exception_file_name_entry,Input_entry,region_var,Type_var,Approval_List_var,
                    Mask_entry,Comment_entry,toggle_state,table_rows,dropdown_values,
                    form_frame,scrollbar,canvas,df,RevisedJSON,table_frame,
                    label1,label2,label3,tab4,table_inner_frame):
        # Retrieve the entered values and process the form data
        global Stat
        engine = create_engine('sqlite:///KnowledgeBase_TestDummy.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        Exception_file_name = Exception_file_name_entry.get()
        Input = Input_entry.get("1.0", "end-1c")
        Input_bytes = Input.encode('utf-8')
        region = region_var.get()
        type_value = Type_var.get()
        approval = Approval_List_var.get()
        pattern = Mask_entry.get("1.0", "end-1c")
        Comment = Comment_entry.get("1.0", "end-1c")
        # component_values = dropdown_var.get()
        table_data = []
        today = datetime.now()
        addValid = toggle_state.get()
        ID = hashlib.sha1(Input_bytes)
        Unique_ID = ID.hexdigest()
        
        # for row in table_rows[0:]:
        #     column1 = row[0].cget("text").strip()
        #     column2 = row[1].cget("text").strip()
        #     column3 = row[2].get()
            
        #     selected_key = next((key for key, val in dropdown_values.items() if val == column3), None)
            
        #     if selected_key is not None:
        #         table_data.append((column1, column2, selected_key))
        #     if not column3:
        #         msg.showerror("Error", "One or More Components are missing!.")
        #         return False
    
            
            
        # Perform validation checks
        if not Exception_file_name:
            msg.showerror("Error", "Exception File Name is required.")
            return False
        if not Input:
            msg.showerror("Error", "Input is required.")
            return False
        if not region:
            msg.showerror("Error", "Region is required.")
            return False
        if not type_value:
            msg.showerror("Error", "Type is required.")
            return False
        if not addValid:
            msg.showerror("Error", "Please Select 'Yes/No' for DataBase Validation")
            return False
        if not approval:
            msg.showerror("Error", "Approval Field is required.")
            return False
        # if not component_values:
        #     messagebox.showerror("Error", "All Components are required.")
        #     return False
        form_data = {
            "Unique_ID": Unique_ID,
            "Exception_file_name": Exception_file_name,
            "Input": Input,
            "Region": region,
            "Type": type_value,
            "Token Pattern": pattern,
            "Approved By": (f"{approval} at {today}"),
            "Comment": Comment,
            "Table Data": table_data
        }
        rejection_data = {
            "Exception_file_name": Exception_file_name,
            "Input": Input,
            "Token Pattern": pattern,
            "Rejected By": (f"{approval} at {today}"),
            "Comment": Comment
        }
        approval_form_instance=approvalform.submission_form()

        print("Approved?" , toggle_state.get())
        
        if toggle_state.get() == "Yes":
            for row in table_rows[0:]:
                column1 = row[0].cget("text").strip()
                column2 = row[1].cget("text").strip()
                column3 = row[2].get()
                
                selected_key = next((key for key, val in dropdown_values.items() if val == column3), None)
                
                if selected_key is not None:
                    table_data.append((column1, column2, selected_key))
                if not column3 or column3 == "Not Selected":
                    msg.showerror("Error", "One or More Components are missing!.")
                    return False
            with open("Validation_DB.txt", 'r+') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
            
                # Append the new data to the existing data list
                existing_data.append(form_data)
                
                # Set the file's current position at the beginning
                file.seek(0)
                
                # Write the updated data back to the file
                json.dump(existing_data, file, indent=4)
                file.truncate()
            
            # messagebox.showinfo("Demo", "Address is added to Validation DataBase")
            print(f"Unique_ID: {Unique_ID}")
            print(f"Exception_file_name: {Exception_file_name}")
            print(f"Input: {Input}")
            print(f"Region: {region}")
            print(f"Type: {type_value}")
            print(f"Token Pattern: {pattern}")
            print(f"Comment: {Comment}")
    
            msg.showinfo("Info", "Address Added to Validation DataBase And Moved to Knowledge Base!")
            print(f"Approved By: {approval} at {today}")
            components = form_frame.winfo_children()
            scrollbar.destroy()
            for component in components:
                component.destroy()
            
            components=table_frame.winfo_children()
            
            for componenet in components:
                component.destroy()
            
            components = canvas.find_all()
            # Remove each component from the canvas
            for component in components:
                canvas.delete(component)
      
            RevisedJSON.pop(0)
            
                
            with open(df[0], 'w', encoding='utf-8') as f:                
                json.dump(RevisedJSON, f)
            
            
            
        elif toggle_state.get() == "No":
            msg.showinfo("Info", "Address is not Approved!")#\nPlease Select a New Exception File")
            # Clear()
            components = form_frame.winfo_children()
            scrollbar.destroy()
            for component in components:
                component.destroy()
            
            components=table_frame.winfo_children()
            
            for componenet in components:
                component.destroy()
            
            components = canvas.find_all()
            # Remove each component from the canvas
            for component in components:
                canvas.delete(component)
            
      
            RevisedJSON.pop(0)
            
                
            with open(df[0], 'w', encoding='utf-8') as f:                
                json.dump(RevisedJSON, f)
            if len(RevisedJSON)>0:
                approval_form_instance.Browse_File(df,True,form_frame,canvas,table_frame,label1,label2,label3,tab4)
                scrollbar.destroy()
            with open("ADDR_Rejection_DB.txt", 'r+') as r_file:
                try:
                    previous_data = json.load(r_file)
                except json.JSONDecodeError:
                    previous_data = []
            
                # Append the new data to the existing data list
                previous_data.append(rejection_data)
                
                # Set the file's current position at the beginning
                r_file.seek(0)
                
                # Write the updated data back to the file
                json.dump(previous_data, r_file, indent=4)
                r_file.truncate()
            print(rejection_data)
                # msg.showinfo("Info", "Address is not Approved")#\nPlease Select a New Exception File")
        print("Table Data:")
        print(table_data)
        for data in table_data:
            print(data)
      
        if toggle_state.get() == "Yes":
            
            i=1
            Def_Dict={}
            for n in table_data:
                if n[2] in Def_Dict.keys():
                    print(Def_Dict[n[2]])
                    Val=Def_Dict[n[2]]
                    Val.append(i)
                    Def_Dict[n[2]]=Val
                else:
                    Def_Dict[n[2]]=[i]
                i+=1
    
            print(Def_Dict)
            # with open('JSONMappingDefault.json', 'r+', encoding='utf-8') as f:
            #     data = json.load(f)
            #     if pattern in data:
            #         result = messagebox.askyesno("MASK Found!", f"Mapping found for Token Pattern : {pattern} in Knowledge Base!\nDo you still want to Overwrite?")
            #         if result:
            #             for x in data:
            #                 if x == pattern:
            #                     data[x] = Def_Dict
            #             # data[pattern] = Def_Dict
            #         else:
            #             pass
            #     else:
            #         data[pattern] = Def_Dict
                    
            #     f.seek(0)        # <--- should reset file position to the beginning.
            #     json.dump(data, f)
            #     f.truncate()# remove remaining part
            existing_mask = session.query(MaskTable).filter_by(mask=pattern).first()
            
            if existing_mask:
                # Check if the mask exists in MappingJSON
                existing_mapping = session.query(MappingJSON).filter_by(mask_index=pattern).first()
            
                if existing_mapping:
                    result = messagebox.askyesno("MASK Found!", f"Mapping found for Token Pattern : {pattern} in Knowledge Base!\nDo you still want to Overwrite?")
                    if result:
                        session.delete(existing_mapping)
                        session.commit()
                    
                        for component, index in Def_Dict.items():
                            new_mapping_entry = MappingJSON(mask_index=pattern, component_index=component, component_value=index)
                            session.add(new_mapping_entry)
                        session.commit()
                    else:
                        pass
            else:
                
                for component, index in Def_Dict.items():
                    new_mapping_entry = MappingJSON(mask_index=pattern, component_index=component, component_value=index)
                    session.add(new_mapping_entry)
                session.commit()
            
            if len(RevisedJSON)>0:
                approval_form_instance.Browse_File(df,True,form_frame,canvas,table_frame,label1,label2,label3,tab4)
                scrollbar.destroy()
                table_inner_frame.destroy()
                return
            return
        
        
        return form_data, rejection_data