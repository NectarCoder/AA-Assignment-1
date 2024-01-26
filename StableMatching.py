from Matching import Match
from StabilityChecker import StabilityChecker 
import sys
import os

def getInputFiles()->list: #pathing in VScode is odd, so this is added to fix it. Shouldn't cause any issues with other IDE's
    path=''
    if getattr(sys,'frozen',False):
        path=os.path.dirname(os.path.realpath(sys.executable))  
    elif __file__:
        path=os.path.dirname(__file__)

    dirPath = os.path.join(path,'MatchingInput') 
    return [os.path.join(dirPath, file) for file in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, file))]

for fullFilePath in getInputFiles():
    applicantdata=[]
    positiondata=[]
    switch=False
    with open(fullFilePath,"r") as rawdata:
        data=rawdata.read()
        compiled=data.split('\n')
        rawdata.close()
    for lines in compiled:
        if lines=='':
            switch=True
        elif switch:
            applicantdata.append([line.strip() for line in lines.split(",")])
        else:
            positiondata.append([line.strip() for line in lines.split(",")])

    matching=Match(applicantdata,positiondata)
    matching.stableMatch()

    matches = matching.getMatches()
    stabilityChecker = StabilityChecker(applicantdata, positiondata, matches)
    unstableMatches = stabilityChecker.stabilityCheckAll()
    if len(unstableMatches) > 0:
        print('Stability Checker complete: Unstable matches found.')
        print(','.join(unstableMatches))
    else:
        print('Stability Checker complete: No unstable matches found.')

    # print Match results
    print(matching)





    

