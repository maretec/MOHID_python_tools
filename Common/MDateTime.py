# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

## this encondes/decodes the MOHID date/time array to/from a float of total time since a reference date, in days 

# Public API

def getTimeStampFromMOHIDDate(MohidDate):
    delta = datetime(int(MohidDate[0]), int(MohidDate[1]), int(MohidDate[2]), int(MohidDate[3]), int(MohidDate[4]), int(MohidDate[5])) - BaseDateTime()
    timeStamp = delta.total_seconds()/timedelta(days=1).total_seconds()
    return timeStamp

def getMOHIDDateFromTimeStamp(timeStamp):
    MD = getDateTimeFromTimeStamp(timeStamp)
    MohidDate = [MD.year, MD.month, MD.day, MD.hour, MD.minute, MD.second]
    return MohidDate

def getDateStringFromTimeStamp(timeStamp):
    return getDateTimeFromTimeStamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")

def getDateStringFromMOHIDDate(MohidDate):
    timeStamp = getTimeStampFromMOHIDDate(MohidDate)
    return getDateTimeFromTimeStamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")


###private functions

def BaseDateTime():
    return datetime(1950, 1, 1, 0, 0, 0)

def getDateTimeFromTimeStamp(timeStamp):
    delta = timedelta(seconds=timeStamp*timedelta (days=1).total_seconds())
    return BaseDateTime() + delta

#API examples
#MOHIDate = [2000, 8, 19, 1, 1, 37]
#print getTimeStampFromMOHIDDate(MOHIDate)
#print getMOHIDDateFromTimeStamp(getTimeStampFromMOHIDDate(MOHIDate))
#print getDateStringFromTimeStamp(getTimeStampFromMOHIDDate(MOHIDate))
#print getDateStringFromMOHIDDate(MOHIDate)