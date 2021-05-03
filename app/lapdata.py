import pandas as pd
import math
import numpy as np

def getData():
   

    attr = ["SteeringWheelAngle", "Speed", "Throttle","Brake", "RPM", "Gear", "Lap", "LapDistPct", "LapDist", "TrackTempCrew", "RRwearM", "LRwearM", "RFwearM", "LFwearM", "LapBestLap", "LapDeltaToBestLap", "LapDeltaToBestLap_OK"]

    dfLaps = pd.read_csv("app/lapdata_Alex_Spa.csv", names=attr)
    dfLaps["SteeringWheelAngle"] = round(dfLaps["SteeringWheelAngle"]*180/math.pi, 2)
    dfLaps["Speed"] = round(dfLaps["Speed"]*3.6, 2)
    dfLaps["RPM"] = round(dfLaps["RPM"])
    dfLaps["Brake"] = round(dfLaps["Brake"], 2)
    dfLaps["Throttle"] = round(dfLaps["Throttle"], 2)
    dfLaps["Gear"] = dfLaps["Gear"].replace(0, np.nan).ffill()
    dfLaps["IsBestLap"] = dfLaps["Lap"] == dfLaps["LapBestLap"].max()

    dfFLap = dfLaps[(dfLaps["Lap"] < 6) & (dfLaps["Lap"] > 0)]
    return dfFLap

def GetTurns():
    Turns = [
        ("T1",390), ("T2",1050), 
        ("T3",1190), ("T4",1280), 
        ("T5",2410), ("T6",2490), 
        ("T7",2650), ("T8",3040), 
        ("T9",3280), ("T10",3800), 
        ("T11",4050), ("T12",4500), 
        ("T13",4640), ("T14",4920),
        ("T15",5140), ("T16",5910),
        ("T17",6170), ("T18",6700),
        ("T19",6750)]
    dfturns = pd.DataFrame(Turns, columns=["Turn", "LapDist"])
    return dfturns