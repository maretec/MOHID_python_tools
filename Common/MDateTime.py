# -*- coding: utf-8 -*-

from datetime import date

def getTimeStampFromDate(MohidDate):
    d0 = date(1950, 1, 1)
    d1 = date(MohidDate[0], MohidDate[1], MohidDate[2])
    delta = d1 - d0
    print delta.days
    
    
getTimeStampFromDate([2000, 8, 19])