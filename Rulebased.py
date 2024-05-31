import re

class RuleBasedNameParser:
    @staticmethod
    def NameParser(line):
        MASK = []  # In String

        USAD_Conversion_Dict = {"GEN_SFX": "", "SUF_TLE": "", "PRE_TLE": "", "GIV_NME": "", "SUR_NME": "", "INITIAL": "", "NA": ""}
        List = USAD_Conversion_Dict.keys()
        FirstPhaseList = []

        fileHandle = open('NamesWordTable.txt', 'r', encoding='utf8')

        NameList = line
        TrackKey = []
        Mask = []
        Combine = ""
        Compare = False
        LoopCheck = 1

        for A in NameList:
            FirstPhaseDict = {}
            NResult = False
            if A == ",":
                O = 0
                Mask.append(Combine)
                Combine = ""
            elif A==" ":
                continue
            elif A!="," and len(A)==1:
                
                NResult=True
                Combine+="I"
                print(A, Combine)
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
                    fields = line.split('|')
                    if A == (fields[0]):
                        NResult = True
                        temp = fields[1]
                        Combine += temp[0]
                        FirstPhaseDict[temp[0]] = A
                        FirstPhaseList.append(FirstPhaseDict)
                        TrackKey.append(temp[0])
                if NResult == False:
                    Combine += "W"
                    TrackKey.append("W")
                    FirstPhaseDict["W"] = A
                    FirstPhaseList.append(FirstPhaseDict)
            if LoopCheck == len(NameList):
                Mask.append(Combine)
            fileHandle.seek(0)
            LoopCheck += 1

        USAD_Mapping = {"GEN_SFX": [], "SUF_TLE": [], "PRE_TLE": [], "GIV_NME": [], "SUR_NME": [], "INITIAL": [], "NA": []}
        Start = 0
        Counts = 0

        Final_Map = [None] * len(FirstPhaseList)
        last_w_index = None
        for idx, key in enumerate(TrackKey):
            if key == "W":
                last_w_index = idx

        for R in USAD_Conversion_Dict:
            for j in range(len(TrackKey)):
                Dictionary = FirstPhaseList[j]
                Key = ""
                Value = ""
                for K, V in Dictionary.items():
                    Key = K
                    Value = V
                if R == "GEN_SFX" and Key == "G":
                    USAD_Mapping["GEN_SFX"].append(j + 1)
                    USAD_Conversion_Dict["GEN_SFX"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "GEN_SFX", Key]
                elif R == "PRE_TLE" and Key == "P":
                    USAD_Mapping["PRE_TLE"].append(j + 1)
                    USAD_Conversion_Dict["PRE_TLE"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "PRE_TLE", Key]
                elif R == "GIV_NME" and Key == "W" and j != last_w_index:
                    USAD_Mapping["GIV_NME"].append(j + 1)
                    USAD_Conversion_Dict["GIV_NME"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "GIV_NME", Key]
                elif R == "SUF_TLE" and Key == "Q":
                    USAD_Mapping["SUF_TLE"].append(j + 1)
                    USAD_Conversion_Dict["SUF_TLE"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "SUF_TLE", Key]
                elif R == "INITIAL" and Key == "I":
                    USAD_Mapping["INITIAL"].append(j + 1)
                    Final_Map[j] = [Value.strip(), "INITIAL", Key]
                elif R == "SUR_NME" and Key == "L":
                    USAD_Mapping["SUR_NME"].append(j + 1)
                    Final_Map[j] = [Value.strip(), "SUR_NME", Key]
        if last_w_index is not None:
            Dictionary = FirstPhaseList[last_w_index]
            Key = ""
            Value = ""
            for K, V in Dictionary.items():
                Key = K
                Value = V
            USAD_Mapping["SUR_NME"].append(last_w_index + 1)
            USAD_Conversion_Dict["SUR_NME"] += " " + Value.strip()
            Final_Map[last_w_index] = [Value.strip(), "SUR_NME", Key]
        for j in range(len(TrackKey)):
            if Final_Map[j] is None:
                Dictionary = FirstPhaseList[j]
                Key = ""
                Value = ""
                for K, V in Dictionary.items():
                    Key = K
                    Value = V
                USAD_Mapping["NA"].append(j + 1)
                USAD_Conversion_Dict["NA"] += " " + Value.strip()
                Final_Map[j] = [Value.strip(), "NA", Key]

        dic = {key: value.strip() for key, value in USAD_Conversion_Dict.items() if value.strip() != ''}
        return Final_Map

