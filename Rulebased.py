import re

class RuleBasedNameParser:
    @staticmethod
    def NameParser(line):
        MASK = []  # In String
        # print("Input Line:", line)
        USAD_Conversion_Dict = {"USNM_GSF": "", "USNM_STL": "", "USNM_PTL": "", "USNM_GNM": "", "USNM_SNM": "", "USNM_NA": ""}
        List = USAD_Conversion_Dict.keys()
        FirstPhaseList = []

        with open('NamesWordTable.txt', 'r', encoding='utf8') as fileHandle:
            NameList = line  # Assuming line is already a list of name tokens
            TrackKey = []
            Mask = []
            Combine = ""
            Compare = False
            LoopCheck = 1
            last_comma_index = None

            for idx, A in enumerate(NameList):
                FirstPhaseDict = {}
                NResult = False
                if A == ",":
                    O = 0
                    Combine = ","
                    Mask.append(Combine)
                    TrackKey.append(",")
                    FirstPhaseDict[","] = A
                    FirstPhaseList.append(FirstPhaseDict)
                    last_comma_index = idx

                elif A == " ":
                    continue
                elif A != "," and len(A) == 1:
                    Combine += "I"
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
                    for clues in fileHandle:
                        fields = clues.split('|')
                        if A == fields[0]:
                            NResult = True
                            temp = fields[1]
                            Combine += temp[0]
                            FirstPhaseDict[temp[0]] = A
                            FirstPhaseList.append(FirstPhaseDict)
                            TrackKey.append(temp[0])
                    if not NResult:
                        Combine += "W"
                        TrackKey.append("W")
                        FirstPhaseDict["W"] = A
                        FirstPhaseList.append(FirstPhaseDict)
                if LoopCheck == len(NameList):
                    Mask.append(Combine)
                fileHandle.seek(0)
                LoopCheck += 1

        # print("Mask:", Mask)
        # print("TrackKey:", TrackKey)
        # print("Combine:", Combine)
        
        USAD_Mapping = {"USNM_GSF": [], "USNM_STL": [], "USNM_PTL": [], "USNM_SNM": [], "USNM_GNM": [], "USNM_NA": []}
        Start = 0
        Counts = 0

        Final_Map = [None] * len(FirstPhaseList)
        last_w_index = None
        for idx, key in enumerate(TrackKey):
            if key == "W":
                last_w_index = idx

        # print("FirstPhaseList:", FirstPhaseList)
        # print("Input Line:", line)
        
        for R in USAD_Conversion_Dict:
            for j in range(len(TrackKey)):
                Dictionary = FirstPhaseList[j]
                # print("Processing Dictionary:", Dictionary)
                Key = ""
                Value = ""
                for K, V in Dictionary.items():
                    Key = K
                    Value = V
                if R == "USNM_GSF" and Key == "G":
                    USAD_Mapping["USNM_GSF"].append(j + 1)
                    USAD_Conversion_Dict["USNM_GSF"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_GSF", Key]
                    
                elif R == "USNM_PTL" and Key == "P":
                    USAD_Mapping["USNM_PTL"].append(j + 1)
                    USAD_Conversion_Dict["USNM_PTL"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_PTL", Key]
                    
                elif R == "USNM_GNM" and Key == "W" and j != last_w_index:
                    if j+1 < len(TrackKey) and j+1 < len(NameList) and TrackKey[j+1] != ',' and TrackKey[j+1] != ' ':
                        USAD_Mapping["USNM_GNM"].append(j + 1)
                        USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                        Final_Map[j] = [Value.strip(), "USNM_GNM", Key]
                    else:
                        USAD_Mapping["USNM_SNM"].append(j + 1)
                        USAD_Conversion_Dict["USNM_SNM"] += " " + Value.strip()
                        Final_Map[j] = [Value.strip(), "USNM_SNM", Key]
                elif R == "USNM_STL" and Key == "Q":
                    USAD_Mapping["USNM_STL"].append(j + 1)
                    USAD_Conversion_Dict["USNM_STL"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_STL", Key]
                    
                elif R == "USNM_GNM" and (Key == "I" or Key == "W"):
                    USAD_Mapping["USNM_GNM"].append(j + 1)
                    USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_GNM", Key]
                    
                elif R == "USNM_SNM" and Key == "L":
                    USAD_Mapping["USNM_SNM"].append(j + 1)
                    USAD_Conversion_Dict["USNM_SNM"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_SNM", Key]
                    
        if last_w_index is not None:
            Dictionary = FirstPhaseList[last_w_index]
            Key = ""
            Value = ""
            for K, V in Dictionary.items():
                Key = K
                Value = V
            if last_comma_index is not None and last_w_index > last_comma_index:
                USAD_Mapping["USNM_GNM"].append(last_w_index + 1)
                USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                Final_Map[last_w_index] = [Value.strip(), "USNM_GNM", Key]
            else:
                USAD_Mapping["USNM_SNM"].append(last_w_index + 1)
                USAD_Conversion_Dict["USNM_SNM"] += " " + Value.strip()
                Final_Map[last_w_index] = [Value.strip(), "USNM_SNM", Key]

        # print("Final_Map before cleanup:", Final_Map)
        
        # Remove None entries
        Final_Map = [entry for entry in Final_Map if entry is not None]
        
        # Adjust Final_Map to exclude comma if necessary
# =============================================================================
#         if ',' in line:
#             comma_index = None
#             for idx, token in enumerate(NameList):
#                 if token == ',':
#                     comma_index = idx
#                     break
#             if comma_index is not None and comma_index < len(Final_Map):
#                 del Final_Map[comma_index]
# =============================================================================
        
        # print("Final_Map after cleanup:", Final_Map)
        
        return Final_Map

# Example usage:
parser = RuleBasedNameParser()
result = parser.NameParser(["John", "R", "Talburt"])
# print(result)

result = parser.NameParser(["Talburt", ",", "R", "John"])
# print(result)
