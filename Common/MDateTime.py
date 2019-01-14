# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

## this encondes/decodes the MOHID date/time array to/from a float of total time since a reference date, in days 

def BaseDateTime():
    return datetime(1950, 1, 1, 0, 0, 0)

def getTimeStampFromDate(MohidDate):
    delta = datetime(MohidDate[0], MohidDate[1], MohidDate[2], MohidDate[3], MohidDate[4], MohidDate[5]) - BaseDateTime()
    timeStamp = delta.total_seconds()/timedelta(days=1).total_seconds()
    return timeStamp

def getMOHIDDateFromTimeStamp(timeStamp):
    delta = timedelta(seconds=timeStamp*timedelta (days=1).total_seconds())
    MD = BaseDateTime() + delta
    MohidDate = [MD.year, MD.month, MD.day, MD.hour, MD.minute, MD.second]
    return MohidDate